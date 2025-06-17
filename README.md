# 🛒 E-commerce API

## RESTful API for product, customer, order, employee management and authentication management with role control

![Entity Relationship Diagram. ](assets/Mermaid%20Entities%20Diagram.png)


## 🧩 Certain behaviors of entities:

- **Client**: Represents the customer who makes purchases within the system. They can register with a username and hashed password; they are assigned a role (client); they can place multiple orders; and they can be deregistered with logical deletion. Their ID is UUID.

- **Employee**: Represents the store's internal staff, who can manage orders, create purchase orders, create products, and update products. They are assigned a role (employee) and are responsible for processing or fulfilling orders. They have limited access to administrative operations. Their ID is generated as a UUID.

- **Role**: This is the entity that defines the different profiles or permissions in the system (ADMIN, EMPLOYEE, CLIENT). It is associated with both client and employee via role_id. It is used internally for route protection, improving access control and providing scalability if more roles are added in the future. Its ID is defined as UUID.

- **Product**: Represents the products that can be sold. They are associated with a category using category_id and are associated with many order details. Their ID is generated as a UUID; their deletion is logically deprecated; they are listed by category and available stock.

- **Category**: This classifies products by type. It can have multiple products, and deletion is due to poor logic. It can be viewed by category, giving the customer greater organization in terms of products and categories. Its ID is defined as UUID.

- **Order**: It represents a transaction in the database when created by the customer. It is associated with a customer and, optionally, with an employee, because sometimes the owner makes the sale. It contains a list of order details (1:N relationship). This gives us a purchase history for the customer and tracks the employee's performance. Terminating the order is logical (called cancel_order). Its ID is defined as UUID.

- **OrderItem**: Represents each product included in an order. It stores the quantity, unit price, and subtotal for that order. If the quantity requested by the customer is greater than the stock, the sale cannot be completed. The total is calculated after completing the details and finalizing the order. Its ID is defined as UUID.

---

# 🔌 Potential integration with another system:

## Integration flow example with a marketplace API (e.g., Mercado Libre)

The following diagram illustrates how an administrator can create a product marked as `sync=True`. If the API call to Mercado Libre succeeds, the product is published automatically. Otherwise, the attempt is queued for retry.


![Potencial Integration Diagram](assets/Potencial%20Integration.png)