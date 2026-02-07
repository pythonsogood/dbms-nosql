# Advanced Databases (NoSQL) Final Project: Online Shop

**Course:** Advanced Databases (NoSQL)  
**Department:** School of Software Engineering  
**Team Members:**  
- **Nurdan Zanabaev** (Frontend)  
- **Sultan** (Backend)

---

## 1. Project Overview

This project is a full-stack E-commerce Web Application designed to demonstrate advanced NoSQL database modeling and high-performance API development using MongoDB. The application allows users to browse products with advanced filtering, manage a shopping cart, place orders, and leave reviews. It features a dedicated Admin Dashboard for real-time sales analytics using MongoDB's Aggregation Framework.

### Key Features
- **User Authentication:** Secure registration and login using JWT and Argon2 hashing.
- **Product Catalog:** Advanced filtering by category, price range, and sorting.
- **Shopping Cart:** Persistent cart management using embedded document patterns.
- **Order Management:** Complete checkout flow and order history.
- **Admin Dashboard:** Aggregated statistics for total revenue and order counts.
- **Reviews System:** Users can rate and review products.

---

## 2. System Architecture

The project follows a **Client-Server Architecture** implemented within a unified FastAPI framework.

- **Backend:** Python (FastAPI) handles business logic, API routing, and database interactions via **Beanie ODM**.
- **Database:** **MongoDB** serves as the primary data store, leveraging document-oriented features like nesting and flexible schemas.
- **Frontend:** Server-side rendered **Jinja2 Templates** combined with **Bootstrap 5** and **Vanilla JavaScript** for dynamic interactivity.

### Tech Stack
| Component | Technology |
|-----------|------------|
| **Language** | Python 3.12 |
| **Framework** | FastAPI |
| **Database** | MongoDB |
| **ODM** | Beanie (Pydantic-based) |
| **Frontend** | Jinja2, Bootstrap, JavaScript |
| **Package Manager** | uv / pip |

---

## 3. Database Schema Description

We utilized complex NoSQL data modeling patterns to optimize for read performance and scalability.

### 3.1 User Collection (`users`)
- **Pattern:** **Subset Pattern / Embedding**. The shopping cart is embedded directly within the user document to avoid joining collections during the checkout flow.
- **Fields:** `username`, `email`, `password_hash`, `cart` (List of embedded items).

### 3.2 Product Collection (`products`)
- **Pattern:** **Reference Pattern**. Products reference their `ProductCategory` to allow for easy category management without updating every product.
- **Fields:** `name`, `price`, `description`, `stock`, `category` (Link), `reviews` (BackLink).

### 3.3 Order Collection (`orders`)
- **Pattern:** **Snapshot Pattern**. When an order is placed, product details (price, name) are copied into the order document. This ensures that future price changes do not affect historical order records.
- **Fields:** `user` (Link), `items` (List of snapshot objects), `total_price`, `status`, `created_at`.

### 3.4 Review Collection (`reviews`)
- **Pattern:** **Reference Pattern**. Reviews are stored in a separate collection to avoid hitting the 16MB document size limit on popular products, while maintaining a BackLink for easy retrieval.

---

## 4. MongoDB Implementation & Queries

The application implements sophisticated MongoDB operations:

- **Advanced Updates via API:**
    - `$push`: Used to add items to the user's embedded cart.
    - `$pull`: Efficiently removes specific items from the cart array.
    - `$inc`: Increments quantity without reading/writing the entire document.
    - `$set`: Updates specific fields like order status.

- **Aggregation Pipeline (Admin Dashboard):**
    ```javascript
    db.orders.aggregate([
        { 
            $group: { 
                _id: null, 
                total_orders: { $sum: 1 }, 
                total_revenue: { $sum: "$total_price" } 
            } 
        }
    ])
    ```

---

## 5. API Documentation

### Auth Module
- `POST /api/auth/register` - Create new account
- `POST /api/auth/login` - Obtain JWT token
- `GET /api/auth/whoami` - Get current session info

### Shop Module
- `GET /api/shop/products` - List products with filters (category, price)
- `GET /api/shop/product/{id}` - Get detailed product view
- `POST /api/shop/product/{id}/review` - Add a review
- `PUT /api/shop/cart/{id}` - Add item to cart
- `PATCH /api/shop/cart/{id}` - Update cart item quantity
- `DELETE /api/shop/cart/{id}` - Remove item from cart

### Templates (Frontend Routes)
- `/` - Home Page
- `/shop` - Product Catalog
- `/cart` - Shopping Cart
- `/admin` - Analytics Dashboard

---

## 6. Indexing and Optimization Strategy

To ensure sub-100ms response times:
1.  **Unique Indexes:** Enforced on `username` and `email` to prevent duplicates and speed up login lookups.
2.  **Compound Indexes:** Implemented on `Product` to support efficient filtering:
    - Index: `{ category: 1, price: 1 }`
    - **Reason:** Users frequently filter by category AND sort/filter by price simultaneously. This index allows MongoDB to fulfill both criteria in a single index scan.
3.  **Projection:** API endpoints return only necessary fields to reduce network overhead.

---

## 7. Contribution of Each Student

### **Nurdan Zanabaev (Frontend)**
- Designed the UI/UX using Bootstrap 5.
- Created all Jinja2 templates (`shop.html`, `cart.html`, etc.).
- Implemented client-side JavaScript for dynamic API interactions (AJAX fetch calls for Cart operations).

### **Sultan (Backend)**
- Architected the MongoDB Database Schema using Beanie.
- Developed the FastAPI Backend and REST endpoints.
- Implemented Security (JWT, Argon2) and Aggregation Logic.

---

## 8. Setup and Installation

1.  **Clone the repository**
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    # OR if using uv
    uv sync
    ```
3.  **Configure Environment:**
    Create a `.env` file in `src/`:
    ```ini
    MONGODB_URI=mongodb://localhost:27017
    JWT_SECRET_KEY=your_secret_key
    ```
4.  **Run the Application:**
    ```bash
    cd src
    python main.py
    ```
5.  **Access:**
    - Web App: `http://localhost:8000`
    - API Docs: `http://localhost:8000/docs`
