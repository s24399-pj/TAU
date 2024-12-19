package pl.pjwstk.orderservice.service;

import org.springframework.stereotype.Service;
import pl.pjwstk.orderservice.exception.PaymentException;
import pl.pjwstk.orderservice.model.Order;

@Service
public class PaymentService {

    public boolean processPayment(Order order) throws PaymentException {
        if (order == null) {
            throw new PaymentException("Zamówienie nie może być null.");
        }
        return true;
    }

}
