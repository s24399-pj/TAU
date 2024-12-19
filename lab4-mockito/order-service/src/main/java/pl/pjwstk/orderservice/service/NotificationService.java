package pl.pjwstk.orderservice.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import pl.pjwstk.orderservice.model.Order;
import pl.pjwstk.orderservice.model.User;

@Slf4j
@Service
public class NotificationService {

    public void sendOrderConfirmation(User user, Order order) {
        log.info("Wysyłanie potwierdzenia zamówienia do użytkownika: {} dla zamówienia: {}", user.getEmail(), order.getId());
    }
}
