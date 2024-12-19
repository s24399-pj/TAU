package pl.pjwstk.orderservice.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pl.pjwstk.orderservice.model.Product;

public interface ProductRepository extends JpaRepository<Product, Long> {
}
