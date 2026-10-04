# BUNYAN

![BUNYAN Logo](./assets/bunyan-logo.png)

BUNYAN is an engineering and property services platform that brings clients, engineers, specialists, and building-material suppliers together in one place.

A client can use the platform to start a full engineering project involving areas such as architecture, civil engineering, electrical/MEP, and interior design. They can also request a consultation with an engineer, find a specialist for a smaller job, browse building materials, place orders, and follow the progress of their requests.

The aim of BUNYAN is to make the process of building, renovating, or finding the right service easier by having the main services in one platform.

---

## Front-End Application

The front-end application and full interface planning can be viewed here:

[BUNYAN Front-End](https://github.com/Mrymhussain/bunyan-front-end)

---

## Getting Started

### Deployed App

Deployment link will be added once the project is deployed.

### Wireframes

The wireframes were planned and created using Excalidraw.

[View Excalidraw](https://excalidraw.com/)

### Back-End Repository

[BUNYAN Back-End](https://github.com/Mrymhussain/bunyan-back-end)

### Front-End Repository

[BUNYAN Front-End](https://github.com/Mrymhussain/bunyan-front-end)

---

## Planning

### ERD

The ERD shows the main entities in the system and how they are related.

![BUNYAN ERD](./assets/bunyan-erd.png)

The main entities planned for the system are:

- User
- Project
- ProjectMember
- Consultation
- ServiceRequest
- ServiceCategory
- Material
- Order
- OrderItem
- Review

---

## Component Hierarchy

The component hierarchy shows how the application is planned and how the main pages and components are connected.

![BUNYAN Component Hierarchy](./assets/component-hierarchy.png)

---

## User Stories

### Users

- As a user, I want to create an account so I can use the platform.
- As a user, I want to sign in so I can access my account.
- As a user, I want to sign out when I finish using the application.
- As a user, I want to view and update my profile.

### Projects

- As a client, I want to start a new project.
- As a client, I want to enter the details of my project.
- As a client, I want to choose the engineering services needed for my project.
- As a client, I want to view all of my projects.
- As a client, I want to view the status and progress of a project.
- As a client, I want to edit my own project.
- As a client, I want to see the professionals working on my project.

### Professionals

- As a client, I want to browse engineers and specialists.
- As a client, I want to search for a professional by specialty.
- As a client, I want to view a professional's profile before requesting a service.
- As a client, I want to view ratings and reviews for professionals.

### Consultations

- As a client, I want to request a consultation with an engineer.
- As a client, I want to choose a preferred date and time for the consultation.
- As a client, I want to view the status of my consultation.
- As an engineer, I want to view consultation requests sent to me.
- As an engineer, I want to update the status of a consultation.

### Services

- As a client, I want to browse services for smaller jobs.
- As a client, I want to find a specialist for a specific service.
- As a client, I want to submit a service request.
- As a client, I want to follow the status of my service request.
- As a specialist, I want to view requests assigned to me.
- As a specialist, I want to update the status of a request.

### Materials and Orders

- As a client, I want to browse building materials.
- As a client, I want to view the price and details of a material.
- As a client, I want to place an order for materials.
- As a client, I want to follow the status of my order.
- As a supplier, I want to add and manage materials.
- As a supplier, I want to view and update orders.

### Reviews

- As a client, I want to leave a rating and review.
- As a client, I want to edit my own review.
- As a client, I want to delete my own review.
---

## Back-End API Endpoints

The back end will use FastAPI. All API endpoints will begin with `/api`.

### Authentication

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api/auth/signup` | Create an account |
| POST | `/api/auth/signin` | Sign in |
| GET | `/api/auth/me` | Get the current signed-in user |

### Users

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/users` | Get users |
| GET | `/api/users/{user_id}` | Get one user |
| PUT | `/api/users/{user_id}` | Update user |
| DELETE | `/api/users/{user_id}` | Delete user |

Users can also be filtered by role or specialty.

### Projects

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/projects` | Get projects |
| POST | `/api/projects` | Create a project |
| GET | `/api/projects/{project_id}` | Get project details |
| PUT | `/api/projects/{project_id}` | Update a project |
| DELETE | `/api/projects/{project_id}` | Delete a project |

### Project Members

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/projects/{project_id}/members` | Get project members |
| POST | `/api/projects/{project_id}/members` | Add project member |
| DELETE | `/api/projects/{project_id}/members/{member_id}` | Remove project member |

### Consultations

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/consultations` | Get consultations |
| POST | `/api/consultations` | Create a consultation |
| GET | `/api/consultations/{consultation_id}` | Get consultation details |
| PUT | `/api/consultations/{consultation_id}` | Update a consultation |
| DELETE | `/api/consultations/{consultation_id}` | Cancel a consultation |

### Service Categories

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/service-categories` | Get service categories |
| POST | `/api/service-categories` | Create a category |
| PUT | `/api/service-categories/{category_id}` | Update a category |
| DELETE | `/api/service-categories/{category_id}` | Delete a category |

### Service Requests

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/service-requests` | Get service requests |
| POST | `/api/service-requests` | Create a service request |
| GET | `/api/service-requests/{request_id}` | Get service request details |
| PUT | `/api/service-requests/{request_id}` | Update a service request |
| DELETE | `/api/service-requests/{request_id}` | Cancel a service request |

### Materials

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/materials` | Get materials |
| POST | `/api/materials` | Add a material |
| GET | `/api/materials/{material_id}` | Get material details |
| PUT | `/api/materials/{material_id}` | Update a material |
| DELETE | `/api/materials/{material_id}` | Delete a material |

Materials can also be filtered by category or supplier.

### Orders

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/orders` | Get orders |
| POST | `/api/orders` | Create an order |
| GET | `/api/orders/{order_id}` | Get order details |
| PUT | `/api/orders/{order_id}` | Update an order |
| DELETE | `/api/orders/{order_id}` | Cancel an order |

### Reviews

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/reviews` | Get reviews |
| POST | `/api/reviews` | Create a review |
| GET | `/api/reviews/{review_id}` | Get review details |
| PUT | `/api/reviews/{review_id}` | Update a review |
| DELETE | `/api/reviews/{review_id}` | Delete a review |

Reviews can also be filtered by user.

---

## Tools Used

The tools used so far for planning and setting up the project are:

- Git
- GitHub
- Visual Studio Code
- Excalidraw

---

## Attributions

External resources that require attribution will be added here during development.