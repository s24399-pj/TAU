package pl.pjwstk.orderservice;

import lombok.SneakyThrows;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import pl.pjwstk.orderservice.exception.PaymentException;
import pl.pjwstk.orderservice.model.Order;
import pl.pjwstk.orderservice.model.OrderItemSlim;
import pl.pjwstk.orderservice.model.OrderStatus;
import pl.pjwstk.orderservice.model.User;
import pl.pjwstk.orderservice.repository.OrderRepository;
import pl.pjwstk.orderservice.repository.ProductRepository;
import pl.pjwstk.orderservice.service.InventoryService;
import pl.pjwstk.orderservice.service.NotificationService;
import pl.pjwstk.orderservice.service.OrderService;
import pl.pjwstk.orderservice.service.PaymentService;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.*;


@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    InventoryService inventoryService;

    @Mock
    PaymentService paymentService;

    @Mock
    NotificationService notificationService;

    @Mock
    OrderRepository orderRepository;

    @Mock
    ProductRepository productRepository;

    @InjectMocks
    OrderService orderService;

    @Captor
    ArgumentCaptor<Order> orderCaptor;

    User user;
    List<OrderItemSlim> orderItems;

    @BeforeEach
    void setUp() {
        user = User.builder()
                .id(1L)
                .name("John Doe")
                .email("john.doe@example.com")
                .address("123 Main St")
                .phoneNumber("123456789")
                .build();

        orderItems = List.of(
                OrderItemSlim.builder().productId("1").quantity((short) 2).build(),
                OrderItemSlim.builder().productId("2").quantity((short) 3).build()
        );
    }

    @Test
    void testCreateOrder_Success() throws PaymentException {

        when(orderRepository.save(any(Order.class))).thenAnswer(invocation -> {
            Order order = invocation.getArgument(0);
            if (order.getId() == null) {
                order.setId(1L);
            }
            return order;
        });

        when(inventoryService.isAvailable(orderItems)).thenReturn(true);

        when(paymentService.processPayment(any(Order.class))).thenReturn(true);
        doNothing().when(inventoryService).reduceStock(orderItems);
        doNothing().when(notificationService).sendOrderConfirmation(eq(user), any(Order.class));

        // Act
        Order result = orderService.createOrder(user, orderItems);

        // Assert
        assertNotNull(result);
        assertEquals(OrderStatus.PAID, result.getStatus());
        assertEquals(1L, result.getId());

        verify(inventoryService, times(1)).isAvailable(orderItems);
        verify(orderRepository, times(2)).save(any(Order.class));
        verify(paymentService, times(1)).processPayment(any(Order.class));
        verify(inventoryService, times(1)).reduceStock(orderItems);
        verify(notificationService, times(1)).sendOrderConfirmation(eq(user), orderCaptor.capture());

        Order capturedOrder = orderCaptor.getValue();
        assertNotNull(capturedOrder);
        assertEquals(1L, capturedOrder.getId());
        assertEquals(OrderStatus.PAID, capturedOrder.getStatus());
    }

    @Test
    @SneakyThrows
    void testCreateOrder_ProductNotAvailable() {
        when(inventoryService.isAvailable(orderItems)).thenReturn(false);

        when(orderRepository.save(any(Order.class))).thenAnswer(invocation -> {
            Order order = invocation.getArgument(0);
            if (order.getId() == null) {
                order.setId(1L);
            }
            return order;
        });

        // Act
        Order result = orderService.createOrder(user, orderItems);

        // Assert
        assertNotNull(result);
        assertEquals(OrderStatus.REJECTED, result.getStatus());
        assertEquals(1L, result.getId());

        verify(inventoryService, times(1)).isAvailable(orderItems);
        verify(orderRepository, times(1)).save(any(Order.class));
        verify(paymentService, never()).processPayment(any(Order.class));
        verify(inventoryService, never()).reduceStock(anyList());
        verify(notificationService, never()).sendOrderConfirmation(any(User.class), any(Order.class));
    }

    @Test
    void testCreateOrder_PaymentFailed() throws PaymentException {
        when(inventoryService.isAvailable(orderItems)).thenReturn(true);
        when(orderRepository.save(any(Order.class))).thenAnswer(invocation -> {
            Order order = invocation.getArgument(0);
            if (order.getId() == null) {
                order.setId(1L);
            }
            return order;
        });

        when(paymentService.processPayment(any(Order.class))).thenReturn(false);

        // Act
        Order result = orderService.createOrder(user, orderItems);

        // Assert
        assertNotNull(result);
        assertEquals(OrderStatus.FAILED, result.getStatus());
        assertEquals(1L, result.getId());

        verify(inventoryService, times(1)).isAvailable(orderItems);
        verify(orderRepository, times(2)).save(any(Order.class)); // Save dla NEW i FAILED
        verify(paymentService, times(1)).processPayment(any(Order.class));
        verify(inventoryService, never()).reduceStock(anyList());
        verify(notificationService, never()).sendOrderConfirmation(any(User.class), any(Order.class));
    }

    @Test
    void testCreateOrder_PaymentException() throws PaymentException {
        when(inventoryService.isAvailable(orderItems)).thenReturn(true);

        when(orderRepository.save(any(Order.class))).thenAnswer(invocation -> {
            Order order = invocation.getArgument(0);
            if (order.getId() == null) {
                order.setId(1L);
            }
            return order;
        });

        when(paymentService.processPayment(any(Order.class))).thenThrow(new PaymentException("Payment processing error"));

        // Act
        Order result = orderService.createOrder(user, orderItems);

        // Assert
        assertNotNull(result);
        assertEquals(OrderStatus.REJECTED, result.getStatus());
        assertEquals(1L, result.getId());

        verify(inventoryService, times(1)).isAvailable(orderItems);
        verify(orderRepository, times(2)).save(any(Order.class));
        verify(paymentService, times(1)).processPayment(any(Order.class));
        verify(inventoryService, never()).reduceStock(anyList());
        verify(notificationService, never()).sendOrderConfirmation(any(User.class), any(Order.class));
    }
}