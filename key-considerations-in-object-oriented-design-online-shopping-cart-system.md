---
title: "Key Considerations in Object-Oriented Design: Online Shopping Cart System"
datePublished: Wed Feb 26 2025 17:52:13 GMT+0000 (Coordinated Universal Time)
cuid: cm8vzwfck000008jv3i33g0tj
slug: key-considerations-in-object-oriented-design-online-shopping-cart-system-6ab7cc9a3697
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1743360618406/9b099ba4-0308-473b-bcb4-9c5b9d17f84f.png

---

Designing an online shopping cart system using object-oriented principles requires careful consideration of scalability, data consistency, and user experience. Below, we explore how to structure the system using object-oriented design principles.

System Design Diagram — Design Online Shopping Cart

### Core Object-Oriented Design

#### Class Design and Relationships

1.  **Core Entities**

The `Product` class encapsulates product details, ensuring that stock availability is checked before an item is added to the cart. This class models a real-world product and enforces basic stock validation rules.

class Product {  
    private String productId;  
    private String name;  
    private double price;  
    private int stockQuantity;  
      
    public Product(String productId, String name, double price, int stockQuantity) {  
        this.productId = productId;  
        this.name = name;  
        this.price = price;  
        this.stockQuantity = stockQuantity;  
    }  
      
    public boolean isAvailable(int quantity) {  
        return stockQuantity >= quantity;  
    }  
      
    public void reduceStock(int quantity) {  
        if (isAvailable(quantity)) {  
            stockQuantity -= quantity;  
        }  
    }  
}

**2\. Shopping Cart**

`ShoppingCart` maintains a list of `CartItem` objects, allowing users to add and remove items. The total price is computed dynamically. This class models the behavior of a real-world shopping cart, keeping track of products and quantities dynamically.

class CartItem {  
    private Product product;  
    private int quantity;  
      
    public CartItem(Product product, int quantity) {  
        this.product = product;  
        this.quantity = quantity;  
    }  
      
    public double getTotalPrice() {  
        return product.getPrice() \* quantity;  
    }  
}

class ShoppingCart {  
    private List<CartItem> items;  
      
    public ShoppingCart() {  
        this.items = new ArrayList<>();  
    }  
      
    public void addItem(Product product, int quantity) {  
        if (product.isAvailable(quantity)) {  
            items.add(new CartItem(product, quantity));  
            product.reduceStock(quantity);  
        }  
    }  
      
    public void removeItem(Product product) {  
        items.removeIf(item -> item.getProduct().equals(product));  
    }  
      
    public double calculateTotal() {  
        return items.stream().mapToDouble(CartItem::getTotalPrice).sum();  
    }  
}

**3\. User and Order Management**

class User {  
    private String userId;  
    private String name;  
    private ShoppingCart cart;  
      
    public User(String userId, String name) {  
        this.userId = userId;  
        this.name = name;  
        this.cart = new ShoppingCart();  
    }  
      
    public ShoppingCart getCart() {  
        return cart;  
    }  
}

class Order {  
    private String orderId;  
    private User user;  
    private List<CartItem> orderedItems;  
    private double totalAmount;  
    private OrderStatus status;  
      
    public Order(String orderId, User user) {  
        this.orderId = orderId;  
        this.user = user;  
        this.orderedItems = new ArrayList<>(user.getCart().getItems());  
        this.totalAmount = user.getCart().calculateTotal();  
        this.status = OrderStatus.PENDING;  
    }  
      
    public void completeOrder() {  
        this.status = OrderStatus.COMPLETED;  
    }  
}

#### Object Relationships and Interactions

*   **One-to-Many Relationship**: `ShoppingCart` contains multiple `CartItem` objects.
*   **Association**: `CartItem` maintains a reference to `Product`, ensuring that a single product instance is shared among cart items.
*   **Encapsulation**: The private attributes of classes ensure that internal states cannot be modified directly, enforcing controlled data manipulation through methods.

#### Design Patterns Used

*   **Singleton Pattern**: Ensures only one instance of `ShoppingCart` exists per user session.
*   **Observer Pattern**: Notifies the inventory system whenever stock levels change.
*   **Strategy Pattern**: Allows different discount strategies to be applied at checkout.
*   **Factory Pattern**: Helps create `Product` and `CartItem` objects dynamically while encapsulating the object creation logic.
*   **Decorator Pattern**: Extends cart functionality (e.g., adding gift wrapping) without modifying existing classes.

#### Example Workflow

1.  **User Adds a Product to Cart**

*   A `Product` instance is fetched from inventory.
*   The system checks availability.
*   If available, a `CartItem` is created and added to `ShoppingCart`.

**2\. User Updates Cart Quantity**

*   The system validates the new quantity.
*   The product stock is updated accordingly.

**3\. User Proceeds to Checkout**

*   The total cost is calculated.
*   Stock availability is verified again.
*   An `Order` object is created for processing payment and delivery.

### Scalability and Performance Considerations

**1\. Handling High Concurrent Requests**

*   **Singleton Pattern for Shopping Cart**: Ensures a single cart instance per user session, preventing unnecessary duplication of resources.
*   **Thread Safety**: Use synchronized methods or `ConcurrentHashMap` to handle concurrent cart modifications, preventing race conditions.
*   **Load Balancing**: Distribute traffic across multiple servers to handle peak loads efficiently.
*   **Database Sharding**: Partition large datasets across multiple database servers to improve query performance.

**2\. Caching Strategies**

*   **Cache Frequently Accessed Products**: Store product details in memory (e.g., using Redis) to reduce database calls and improve response time.
*   **Use LRU Cache for Popular Products**: Implement Least Recently Used (LRU) cache to prioritize frequently accessed items while evicting less popular ones.
*   **Session-Based Caching**: Cache user-specific shopping cart data in memory to reduce database read operations.

#### Consistency and Data Integrity

**1\. Ensuring Cart Data Consistency**

*   **Optimistic Locking**: Avoids excessive locks but checks data validity before committing, ensuring multiple users do not override each other’s changes.
*   **Event Sourcing**: Uses an event-driven model to track state changes and replay events in case of failures.
*   **ACID Transactions**: Ensure database consistency by enforcing atomic operations when modifying the cart.

**2\. Data Synchronization**

*   **Observer Pattern**: Notifies other services (e.g., inventory system) about cart changes asynchronously.
*   **Message Queues**: Use Kafka or RabbitMQ for distributed transaction processing, ensuring changes are propagated efficiently.

### User Experience and Usability

#### **1\. Real-Time Updates**

*   **WebSockets for Live Inventory Updates**: Ensures users receive real-time stock updates without needing to refresh the page.
*   **Debounced API Calls for Cart Modifications**: Reduces redundant updates by batching user actions before sending requests to the server.
*   **Progressive Enhancement**: Gracefully degrade features for users on slow networks while maintaining a functional shopping experience.

#### **2\. Personalized Recommendations**

**Strategy Pattern for Different Recommendation Methods**:

*   **Collaborative Filtering**: Recommends products based on user behavior and purchase history.
*   **Content-Based Filtering**: Uses product attributes and user preferences to suggest relevant items.
*   **Hybrid Approach**: Combines collaborative and content-based filtering for better accuracy.
*   **A/B Testing for Recommendation Effectiveness**: Implement A/B testing to measure how well different recommendation algorithms influence user engagement and conversions.

Full Answer: [https://bugfree.ai/practice/object-oriented-design/online-shopping-cart/solutions/W-yhF0fNOlBHtRuC](https://bugfree.ai/practice/object-oriented-design/online-shopping-cart/solutions/W-yhF0fNOlBHtRuC)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1743360616802/e08ea37a-fbad-419e-b50d-42b18e8aaf64.png)

System Design Solution — Design Online Shopping Cart