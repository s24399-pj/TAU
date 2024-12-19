package pl.pjwstk.orderservice.service;

import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.experimental.FieldDefaults;
import org.springframework.stereotype.Service;
import pl.pjwstk.orderservice.model.OrderItemSlim;
import pl.pjwstk.orderservice.model.Product;
import pl.pjwstk.orderservice.repository.ProductRepository;

import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@FieldDefaults(makeFinal = true, level = AccessLevel.PRIVATE)
public class InventoryService {

    ProductRepository productRepository;

    public boolean isAvailable(List<OrderItemSlim> orderItems) {
        List<OrderItemSlim> items = Optional.ofNullable(orderItems)
                .orElseGet(Collections::emptyList)
                .stream()
                .filter(Objects::nonNull)
                .toList();

        if (items.isEmpty()) {
            return false;
        }

        for (OrderItemSlim item : items) {
            Long productId;
            try {
                productId = Long.parseLong(item.getProductId());
            } catch (NumberFormatException e) {
                return false;
            }

            Optional<Product> productOpt = productRepository.findById(productId);
            if (productOpt.isEmpty()) {
                return false;
            }

            Product product = productOpt.get();
            if (product.getStock() < item.getQuantity()) {
                return false;
            }
        }

        return true;
    }

    public void reduceStock(List<OrderItemSlim> orderItems) {
        List<OrderItemSlim> items = Optional.ofNullable(orderItems)
                .orElseGet(Collections::emptyList)
                .stream()
                .filter(Objects::nonNull)
                .collect(Collectors.toList());

        for (OrderItemSlim item : items) {
            Long productId;
            try {
                productId = Long.parseLong(item.getProductId());
            } catch (NumberFormatException e) {
                // Niepoprawne ID produktu, pomijamy ten element
                continue;
            }

            Optional<Product> productOpt = productRepository.findById(productId);
            if (productOpt.isPresent()) {
                Product product = productOpt.get();
                int newStock = product.getStock() - item.getQuantity();
                product.setStock(newStock);
                productRepository.save(product);
            }
        }
    }
}
