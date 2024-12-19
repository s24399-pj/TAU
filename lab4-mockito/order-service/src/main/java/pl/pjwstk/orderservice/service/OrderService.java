package pl.pjwstk.orderservice.service;

import jakarta.transaction.Transactional;
import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;
import org.springframework.stereotype.Service;
import pl.pjwstk.orderservice.exception.PaymentException;
import pl.pjwstk.orderservice.model.Order;
import pl.pjwstk.orderservice.model.OrderItemSlim;
import pl.pjwstk.orderservice.model.OrderStatus;
import pl.pjwstk.orderservice.model.User;
import pl.pjwstk.orderservice.repository.OrderRepository;

import java.util.List;

@Service
@RequiredArgsConstructor
@FieldDefaults(makeFinal = true, level = AccessLevel.PRIVATE)
public class OrderService {

    InventoryService inventoryService;
    PaymentService paymentService;
    NotificationService notificationService;
    OrderRepository orderRepository;

    @Transactional
    public Order createOrder(User user, List<OrderItemSlim> orderItems) {
        if (!inventoryService.isAvailable(orderItems)) {
            Order failedOrder = Order.builder()
                    .user(user)
                    .status(OrderStatus.REJECTED)
                    .build();
            return orderRepository.save(failedOrder);
        }

        Order newOrder = Order.builder()
                .user(user)
                .status(OrderStatus.NEW)
                .build();
        orderRepository.save(newOrder);

        try {
            boolean paymentSuccess = paymentService.processPayment(newOrder);
            if (paymentSuccess) {
                newOrder.setStatus(OrderStatus.PAID);
                orderRepository.save(newOrder);
                inventoryService.reduceStock(orderItems);

                notificationService.sendOrderConfirmation(user, newOrder);
            } else {
                newOrder.setStatus(OrderStatus.FAILED);
                orderRepository.save(newOrder);
            }
        } catch (PaymentException e) {
            newOrder.setStatus(OrderStatus.REJECTED);
            orderRepository.save(newOrder);
        }

        return newOrder;
    }
}
