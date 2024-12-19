package pl.pjwstk.orderservice.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pl.pjwstk.orderservice.model.Order;

public interface OrderRepository extends JpaRepository<Order, Long> {
}
