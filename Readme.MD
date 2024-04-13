## Title: Online Movie Ticket Booking System using Django and DRF

## Table of Contents
- [Introduction](#introduction)
- [Cloning the Repository](#cloning-the-repository)
- [Installation](#installation)
- [Starting Docker](#starting-docker)
- [Building and Running the Application](#building-and-running-the-application)
- [API Documentation](#api-documentation)
- [Endpoints](#endpoints)
- [Testing](#testing)
- [Design Decisions and Featues](#design-decisions-and-features)

## Warning: Please change your email and password in the settings as password is blank

## Cloning the Repository
To clone the Git repository containing the application code:

```shell
git clone https://github.com/Suryakiran09/valor_assignment.git
cd valor_assignment
```

## Introduction
My Application is a web service that provides various features using RESTful APIs. This document serves as a guide to install, run, and interact with the application using Docker and Docker Compose.

## Installation
To get started with the application, you need to have Docker and Docker Compose installed on your system.

- **Docker:** Install Docker Desktop for Windows from the [official Docker website](https://www.docker.com/get-started).
- **Docker Compose:** Docker Compose is installed automatically with Docker Desktop. Check the [installation guide](https://docs.docker.com/compose/install/) for more information.

## Starting Docker
After installing Docker, Docker Desktop should automatically start on startup. You can check if Docker is running by looking for the Docker icon in the system tray.

## Building and Running the Application
To build and run the application, follow these steps:

1. **Clone the Repository:**
    Clone the Git repository containing the application code:

    ```shell
    git clone https://github.com/Suryakiran09/valor_assignment.git
    cd valor_assignment
    ```

2. **Build the Application:**
    Use Docker Compose to build the application:

    ```shell
    docker-compose build
    ```

3. **Start the Application:**
    Start the application using Docker Compose:

    ```shell
    docker-compose up
    ```

The application will now be running and accessible at `http://localhost:8080/`.

## API Documentation

The API documentation can be accessed at the following URLs:

- **Swagger UI:** [Swagger UI](http://localhost:8000/) - [http://localhost:8000/]
- **ReDoc:** [ReDoc](http://localhost:8000/redoc/) - [http://localhost:8000/redoc/]

## Endpoints
Here are the available API endpoints with dummy JSON data for each endpoint:

This is the documentation for the Movie Ticket Booking API, which allows users to manage movies, theaters, showtimes, reservations, and purchased tickets.


| **Endpoint** | **Method** | **Description** | **Request Headers** | **Request Body** | **Filters** |
| --- | --- | --- | --- | --- | --- |
| `/movies/` | GET | List Movies | `Authorization: Bearer <access_token>` | N/A | Search by `title`, `director`, `genre` |
| `/movies/` | POST | Create Movie | `Content-Type: application/json`, `Authorization: Bearer <access_token>` | ```json { "title": "Dummy Movie", "director": "Dummy Director", "genre": "Dummy Genre", "release_date": "2024-01-01", "duration": 120, "synopsis": "Dummy synopsis for the movie." } ``` | N/A |
| `/movies/<int:pk>/` | GET | Retrieve Movie | `Authorization: Bearer <access_token>` | N/A | N/A |
| `/theaters/` | GET | List Theaters | `Authorization: Bearer <access_token>` | N/A | N/A |
| `/theaters/` | POST | Create Theater | `Content-Type: application/json`, `Authorization: Bearer <access_token>` | ```json { "name": "Dummy Theater", "location": "Dummy Location", "capacity": 200 } ``` | N/A |
| `/theaters/<int:pk>/` | GET | Retrieve Theater | `Authorization: Bearer <access_token>` | N/A | N/A |
| `/showtimes/` | GET | List Showtimes | `Authorization: Bearer <access_token>` | N/A | Order by `date_time` |
| `/showtimes/` | POST | Create Showtime | `Content-Type: application/json`, `Authorization: Bearer <access_token>` | ```json { "date_time": "2024-06-01T12:00:00", "movie": 1, "theater": 1 } ``` | N/A |
| `/showtimes/<int:pk>/` | GET | Retrieve Showtime | `Authorization: Bearer <access_token>` | N/A | N/A |
| `/showtimes/<int:pk>/available-seats/` | GET | Available Seats for Showtime | `Authorization: Bearer <access_token>` | N/A | N/A |
| `/reservations/` | GET | List Reservations | `Authorization: Bearer <access_token>` | N/A | N/A |
| `/reservations/<int:pk>/reserve/` | POST | Reserve Seats | `Content-Type: application/json`, `Authorization: Bearer <access_token>` | ```json { "seats": [1, 2, 3] } ``` | N/A |
| `/reservations/<int:pk>/purchase/` | POST | Purchase Tickets | `Authorization: Bearer <access_token>` | N/A | N/A |
| `/purchased_tickets/` | GET | List Purchased Tickets | `Authorization: Bearer <access_token>` | N/A | N/A |
| `/accounts/register/` | POST | User Registration | `Content-Type: application/json` | ```json { "username": "dummyuser", "email": "dummyuser@example.com", "password": "dummypassword" } ``` | N/A |
| `/accounts/login/` | POST | User Login | `Content-Type: application/json` | ```json { "username": "dummyuser", "password": "dummypassword" } ``` | N/A |

- Search filters: The list movies endpoint supports search filters on `title`, `director`, and `genre`.
- Ordering filters: The list showtimes endpoint supports ordering by `date_time`.

## Testing

An accompanying ipython notebook called `testing.ipynb` has been provided demonstrating examples illustrating interaction possibilities offered by various end points presented earlier. Users can modify these snippets accordingly experimenting diverse combinations expanding knowledge horizon gradually yet steadily mastering concepts one step at a time.

## Design Decisions and Features

### 1. Models

The application uses the following Django models to represent the entities involved in the movie ticket booking system:

- **Movie**: Represents a movie with attributes such as `title`, `director`, `genre`, `release_date`, `duration`, and `synopsis`.
- **Theater**: Represents a theater with attributes such as `name`, `location`, and `capacity`.
- **Showtime**: Represents a showtime with attributes such as `date_time`, `movie`, `theater`, and `available_seats`.
- **Reservation**: Represents a reservation made by a user for a particular showtime with attributes such as `user`, `showtime`, `reserved_seats`, and `is_purchased`.

These models were chosen to mirror the core components of a movie ticket booking system and their relationships.

### 2. API Endpoints and Implementation

The API endpoints allow users to manage movies, theaters, showtimes, reservations, and purchased tickets. They are implemented using Django REST Framework (DRF) views and serializers.

- **CRUD Operations**: Most models support Create, Read, Update, and Delete (CRUD) operations via DRF views such as `ListCreateAPIView` and `RetrieveAPIView`.
- **Reservations and Ticket Purchasing**: The API provides endpoints for reserving seats and purchasing tickets, ensuring only the appropriate user can reserve or purchase tickets.

### 3. Authentication and Security

The application uses two types of authentication:

- **Basic Authentication**: Used for some of the API endpoints, providing simple username/password authentication.
- **JWT Authentication**: Used for more secure authentication and session management. It provides token-based authentication for API requests.

Security mechanisms in place include:

- **Permissions**: DRF's `IsAuthenticated` and `AllowAny` permission classes are used to control access to endpoints.
- **Authorization**: Ensures only the appropriate user can access or modify their data.

### 4. Pagination, Search, and Ordering

The application incorporates various features to enhance data management and user experience:

- **Pagination**: DRF's pagination classes can be used to control the number of results returned in list views, providing a more manageable data size.
- **Search**: Search filters are used in the `ListCreateAPIView` views to allow searching based on certain fields (e.g., `title`, `director`, `genre` for movies).
- **Ordering**: Ordering filters are used in list views to allow sorting based on specific fields (e.g., `date_time` for showtimes).

### 5. Email Functionality

After a user successfully purchases tickets, an email notification is sent to the user's registered email address. This is implemented in the `purchase_tickets` view using Django's `send_mail` function, ensuring the user is informed of their purchase.

### Trade-Offs

- **Simplicity vs. Flexibility**: The application design prioritizes simplicity and ease of use over extensive customization.
- **Performance vs. Detail**: Pagination and filtering improve performance but may limit the detail of results.

The design decisions and features are based on providing a straightforward and efficient movie ticket booking system that can scale with user needs.