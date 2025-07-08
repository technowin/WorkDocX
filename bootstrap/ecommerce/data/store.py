user1 = "/static/images/users/avatar-1.jpg"
user2 = "/static/images/users/avatar-2.jpg"
user3 = "/static/images/users/avatar-3.jpg"
user4 = "/static/images/users/avatar-4.jpg"
user5 = "/static/images/users/avatar-5.jpg"
user6 = "/static/images/users/avatar-6.jpg"
user7 = "/static/images/users/avatar-7.jpg"
user8 = "/static/images/users/avatar-8.jpg"
user9 = "/static/images/users/avatar-9.jpg"
user10 = "/static/images/users/avatar-10.jpg"


product1 = "/static/images/products/product-1.jpg"
product2 = "/static/images/products/product-2.jpg"
product3 = "/static/images/products/product-3.jpg"
product4 = "/static/images/products/product-4.jpg"
product5 = "/static/images/products/product-5.jpg"
product6 = "/static/images/products/product-6.jpg"


productStatus = {
    "active": {"name": "Active", "color": "success"},
    "deactive": {"name": "Deactive", "color": "danger"},
}

productsDict = [
    {
        "id": 1,
        "img": product6,
        "name": "Adirondack Chair",
        "category": "Aeron Chairs",
        "added_date": "07/07/2018",
        "quantity": "652",
        "price": "$65.94",
        "status":  productStatus["active"],
        "rating": 5,
    },
    {
        "id": 2,
        "img": product1,
        "name": "Amazing Modern Chair",
        "category": "Aeron Chairs",
        "added_date": "09/12/2018",
        "quantity": "254",
        "price": "$148.66",
        "status":  productStatus["active"],
        "rating": 5,
    },
    {
        "id": 3,
        "img": product2,
        "name": "Bean Bag Chair",
        "category": "Wooden Chairs	",
        "added_date": "06/30/2018",
        "quantity": "1,021",
        "price": "$99",
        "status":  productStatus["deactive"],
        "rating": 5,
    },
    {
        "id": 4,
        "img": product4,
        "name": "Biblio Plastic Armchair",
        "category": "Wooden Chairs",
        "added_date": "09/08/2018	",
        "quantity": "1,874",
        "price": "$8.99",
        "status":  productStatus["active"],
        "rating": 4.5,
    },
    {
        "id": 5,
        "img": product3,
        "name": "Bootecos Plastic Armchair",
        "category": "Wing Chairs",
        "added_date": "07/15/2018",
        "quantity": "485",
        "price": "$148.66",
        "status":  productStatus["deactive"],
        "rating": 4.5,
    },
    {
        "id": 6,
        "img": product3,
        "name": "Branded Wooden Chair",
        "category": "Dining Chairs",
        "added_date": "09/05/2018",
        "quantity": "2,541",
        "price": "$68.32",
        "status":  productStatus["active"],
        "rating": 4,
    },
    {
        "id": 7,
        "img": product5,
        "name": "Cardan Armchair",
        "category": "Plastic Armchair",
        "added_date": "08/02/2018	",
        "quantity": "26",
        "price": "$59.69",
        "status":  productStatus["active"],
        "rating": 5,
    },
    {
        "id": 8,
        "img": product4,
        "name": "Designer Awesome Chair",
        "category": "Baby Chairs	",
        "added_date": "08/23/2018",
        "quantity": "3,540",
        "price": "$112.00",
        "status":  productStatus["active"],
        "rating": 3.5,
    },
    {
        "id": 9,
        "img": product4,
        "name": "Eames Lounge Chair",
        "category": "Baby Chairs",
        "added_date": "05/06/2018",
        "quantity": "1,254",
        "price": "$39.5",
        "status":  productStatus["active"],
        "rating": 4.5,
    },
    {
        "id": 10,
        "img": product5,
        "name": "Farthingale Chair",
        "category": "Plastic Armchair",
        "added_date": "04/09/2018",
        "quantity": "524",
        "price": "$78.66",
        "status":  productStatus["deactive"],
        "rating": 4.5,
    },
    {
        "id": 11,
        "img": product3,
        "name": "The butterfly chair",
        "category": "Dining Chairs",
        "added_date": "06/19/2018",
        "quantity": "874",
        "price": "$58",
        "status":  productStatus["active"],
        "rating": 4.5,
    },
    {
        "id": 12,
        "img": product6,
        "name": "Unpowered aircraft",
        "category": "Wing Chairs",
        "added_date": "03/24/2018",
        "quantity": "204",
        "price": "$49",
        "status":  productStatus["deactive"],
        "rating": 4.5,
    },
]

productDetailsDict = {
    "main_img": product5,
    "images": [product1, product6, product3],
    "name": "Amazing Modern Chair (Orange)",
    "added_date": "09/12/2018",
    "rating": 5,
    "status": {"name": "Instock", "color": "success"},
    "retail_price": "$139.58",
    "quantity": 1,
    "description": "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English.",
    "available_stock": "1784",
    "number_of_orders": "5,458",
    "revenue": "$8,57,014",
}
outletsDict = [
    {
        "name": "ASOS Ridley Outlet - NYC",
        "price": "$139.58",
        "stoke": {"quantity": 478, "color": "success", "pr": 56},
        "revenue": "$1,89,547",
    },
    {
        "name": "Marco Outlet - SRT",
        "price": "$149.99",
        "stoke": {"quantity": 73, "color": "danger", "pr": 16},
        "revenue": "$87,245",
    },
    {
        "name": "Chairtest Outlet - HY",
        "price": "$135.87",
        "stoke": {"quantity": 781, "color": "success", "pr": 72},
        "revenue": "$5,87,478",
    },
    {
        "name": "Nworld Group - India",
        "price": "$159.89",
        "stoke": {"quantity": 815, "color": "success", "pr": 89},
        "revenue": "$55,781",
    },
]

paymentStatus = {
    "paid": {"name": "Paid", "color": "success", "icon": "mdi-bitcoin"},
    "awaiting_authorization": {"name": "Awaiting Authorization", "color": "warning", "icon": "mdi-timer-sand"},
    "payment_failed": {"name": " Payment Failed", "color": "danger", "icon": "mdi-cancel"},
    "unpaid": {"name": "Unpaid", "color": "info", "icon": "mdi-cash"},
}

orderStatus = {
    "shipped": {"name": "Shipped", "color": "info"},
    "processing": {"name": "Processing", "color": "warning"},
    "delivered": {"name": "Delivered", "color": "success"},
    "cancelled": {"name": "Cancelled", "color": "danger"},
}

ordersDict = [
    {
        "id": 1,
        "order_id": "#BM9708",
        "date": "August 05 2018",
        "time": "10:29 PM",
        "payment_status": paymentStatus["paid"],
        "total": "$176.41",
        "payment_method": "Mastercard",
        "order_status": orderStatus["shipped"]
    },
    {
        "id": 2,
        "order_id": "#BM9707",
        "date": "August 04 2018",
        "time": "08:18 AM",
        "payment_status": paymentStatus["awaiting_authorization"],
        "total": "$1,458.65",
        "payment_method": "Visa",
        "order_status": orderStatus["processing"]
    },
    {
        "id": 3,
        "order_id": "#BM9706",
        "date": "August 04 2018",
        "time": "10:29 PM",
        "payment_status": paymentStatus["paid"],
        "total": "$801.99",
        "payment_method": "Credit Card",
        "order_status": orderStatus["processing"]
    },
    {
        "id": 4,
        "order_id": "#BM9705",
        "date": "August 03 2018",
        "time": "07:56 AM",
        "payment_status": paymentStatus["paid"],
        "total": "$215.35",
        "payment_method": "Mastercard",
        "order_status": orderStatus["delivered"]
    },
    {
        "id": 5,
        "order_id": "#BM9704",
        "date": "May 22 2018",
        "time": "07:22 PM",
        "payment_status": paymentStatus["payment_failed"],
        "total": "$2,514.36",
        "payment_method": "Paypal",
        "order_status": orderStatus["cancelled"]
    },
    {
        "id": 6,
        "order_id": "#BM9703",
        "date": "April 02 2018",
        "time": "03:02 AM",
        "payment_status": paymentStatus["paid"],
        "total": "$183.20",
        "payment_method": "Payoneer",
        "order_status": orderStatus["shipped"]
    },
    {
        "id": 7,
        "order_id": "#BM9702",
        "date": "March 18 2018",
        "time": "11:19 PM",
        "payment_status": paymentStatus["awaiting_authorization"],
        "total": "$1,768.41",
        "payment_method": "Visa",
        "order_status": orderStatus["processing"]
    },
    {
        "id": 8,
        "order_id": "#BM9701",
        "date": "February 01 2018",
        "time": "07:22 AM",
        "payment_status": paymentStatus["unpaid"],
        "total": "$3,582.99",
        "payment_method": "Paypal",
        "order_status": orderStatus["shipped"]
    },
    {
        "id": 9,
        "order_id": "#BM9700",
        "date": "January 22 2018",
        "time": "08:09 PM",
        "payment_status": paymentStatus["paid"],
        "total": "$923.95",
        "payment_method": "Credit Card",
        "order_status": orderStatus["delivered"]
    },
    {
        "id": 10,
        "order_id": "#BM9699",
        "date": "January 17 2018",
        "time": "02:30 PM",
        "payment_status": paymentStatus["paid"],
        "total": "$5,177.68",
        "payment_method": "Mastercard",
        "order_status": orderStatus["shipped"]
    },
]

orderDict = {
    "order_id": "#12537",
    "status": {"name": "packed", "order": 2},
    "items": [
        {
            "name": "The Military Duffle Bag",
            "quantity": 3,
            "price": "$128",
            "total": "$384",
        },
        {
            "name": "Mountain Basket Ball",
            "quantity": 1,
            "price": "$199",
            "total": "$199",
        },
        {
            "name": "Wavex Canvas Messenger Bag",
            "quantity": 5,
            "price": "$180",
            "total": "$900",
        },
        {
            "name": "The Utility Shirt",
            "quantity": 2,
            "price": "$79",
            "total": "$158",
        },
    ],
    "order_summary": {
        "grand_total": "$1641",
        "shipping_charge": "$23",
        "estimated_tax": "$19.22",
        "total": "$1683.22",
    },
    "shipping_information": {
        "name": "Stanley Jones",
        "address1": "795 Folsom Ave, Suite 600",
        "address2": "San Francisco, CA 94107",
        "p_number": "(123) 456-7890",
        "m_number": "(+01) 12345 67890",
    },
    "billing_information": {
        "payment_type": "Credit Card",
        "provider": "Visa ending in 2851",
        "valid_date": "02/2020",
        "cvv":  "xxx",
    },
    "delivery_info": {
        "type": "UPS Delivery",
        "order_id": "xxxx235",
        "payment_mode": "COD",
    }
}

customerStatus = {
    "blocked": {"name": "Blocked", "color": "danger"},
    "active": {"name": "Active", "color": "success"}
}

customersDict = [
    {
        "id": 1,
        "avatar": user2,
        "name": "Rory Seekamp",
        "phone": "078 5054 8877",
        "email": "roryamp@dayrep.com",
        "location": "United States",
        "created_date": "03/24/2018",
        "status": customerStatus["blocked"],
    },
    {
        "id": 2,
        "avatar": user10,
        "name": "Dean Smithies",
        "phone": "077 6157 4248",
        "email": "deanes@dayrep.com",
        "location": "Singapore",
        "created_date": "04/09/2018",
        "status": customerStatus["active"],
    },
    {
        "id": 3,
        "avatar": user9,
        "name": "Anna Ciantar",
        "phone": "(216) 76 298 896",
        "email": "annac@hotmai.us",
        "location": "Philippines",
        "created_date": "05/06/2018",
        "status": customerStatus["active"],
    },
    {
        "id": 4,
        "avatar": user1,
        "name": "Labeeb Ghali",
        "phone": "050 414 8778",
        "email": "labebswad@teleworm.us",
        "location": "United Kingdom",
        "created_date": "06/19/2018",
        "status": customerStatus["active"],
    },
    {
        "id": 5,
        "avatar": user3,
        "name": "Kathryn S. Collier",
        "phone": "828-216-2190",
        "email": "collier@jourrapide.com",
        "location": "Canada",
        "created_date": "06/30/2018",
        "status": customerStatus["blocked"],
    },
    {
        "id": 6,
        "avatar": user4,
        "name": "Paul J. Friend",
        "phone": "937-330-1634",
        "email": "pauljfrnd@jourrapide.com",
        "location": "New York",
        "created_date": "07/07/2018",
        "status": customerStatus["active"],
    },
    {
        "id": 7,
        "avatar": user5,
        "name": "Zara Raws",
        "phone": "(02) 75 150 655",
        "email": "austin@dayrep.com",
        "location": "Germany",
        "created_date": "07/15/2018",
        "status": customerStatus["active"],
    },
    {
        "id": 8,
        "avatar": user7,
        "name": "Jenny C. Gero",
        "phone": "078 7173 9261",
        "email": "jennygero@teleworm.us",
        "location": "Lesotho",
        "created_date": "08/02/2018",
        "status": customerStatus["blocked"],
    },
    {
        "id": 9,
        "avatar": user8,
        "name": "Edward Roseby",
        "phone": "078 6013 3854",
        "email": "edwardR@armyspy.com",
        "location": "Monaco",
        "created_date": "08/23/2018",
        "status": customerStatus["active"],
    },
    {
        "id": 10,
        "avatar": user6,
        "name": "Annette P. Kelsch",
        "phone": "(+15) 73 483 758",
        "email": "annette@email.net",
        "location": "India",
        "created_date": "09/05/2018",
        "status": customerStatus["active"],
    },
    {
        "id": 11,
        "avatar": user1,
        "name": "Timothy Kauper",
        "phone": "(216) 75 612 706",
        "email": "thykauper@rhyta.com",
        "location": "Denmark",
        "created_date": "09/08/2018",
        "status": customerStatus["blocked"],
    },
    {
        "id": 12,
        "avatar": user3,
        "name": "Bryan J. Luellen",
        "phone": "215-302-3376",
        "email": "bryuellen@dayrep.com",
        "location": "New York",
        "created_date": "09/12/2018",
        "status": customerStatus["active"],
    },
]


shoppingCartDict = {
    "order_summary": {
        "grand_total": "$1571.19",
        "discount": "-$157.11",
        "shipping_charge": "$25",
        "estimated_tax": "$19.22",
        "total": "$1458.3",
    },
    "coupon_code": "HYPBM",
    "discount": "10%",
}

shoppingCartProductsDict = [
    {
        "id": 1,
        "name": "Amazing Modern Chair",
        "img": product1,
        "size": "Large",
        "color": "Light Green",
        "price": "$148.66",
        "quantity": 5,
        "total": "$743.30",
    },
    {
        "id": 2,
        "name": "Biblio Plastic Armchair",
        "img": product2,
        "size": "Small",
        "color": "Brown",
        "price": "$99.00",
        "quantity": 2,
        "total": "$198.00",
    },
    {
        "id": 3,
        "name": "Designer Awesome Chair",
        "img": product3,
        "size": "Medium",
        "color": "Green",
        "price": "$49.99",
        "quantity": 10,
        "total": "$499.90",
    },
    {
        "id": 4,
        "name": "Unpowered aircraft",
        "img": product5,
        "size": "Large",
        "color": "Orange",
        "price": "$129.99",
        "quantity": 1,
        "total": "$129.99",
    },
]


checkoutOredrsDict = [
    {
        "id" : 1,
        "name" : "Amazing Modern Chair",
        "img" : product1,
        "quantity" :  5,
        "price" : "$148.66",
        "total" : "$743.30",
    },
    {
        "id" : 2,
        "name" : "Designer Awesome Chair",
        "img" : product2,
        "quantity" :  2,
        "price" : "$99.00",
        "total" : "$198.00",
    },
    {
        "id" : 3,
        "name" : "Biblio Plastic Armchair",
        "img" : product3,
        "quantity" :  1,
        "price" : "$129.99",
        "total" : "$129.99",
    }
]
checkoutOrderSummaryDict = {
    "sub_total" : "$1071.29",
    "shipping" : "FREE",
    "total" : "$1071.29",
}


checkoutHomeAddressDict = {
        "id" : 1,
        "type" : "Home",
        "name" : "Stanley Jones",
        "a_l1" : "795 Folsom Ave, Suite 600",
        "a_l2" : "San Francisco, CA 94107",
        "p_number" : "(123) 456-7890",
    }

checkoutOfficeAddressDict = {
        "id" : 2,
        "type" : "Office",
        "name" : "Stanley Jones",
        "a_l1" : "795 Folsom Ave, Suite 600",
        "a_l2" : "San Francisco, CA 94107",
        "p_number" : "(123) 456-7890",
    }

checkoutShippingMethodsDict = {
    "standard_delivery_amount" : "FREE",
    "standard_delivery_days" : "5-7",
    "fast_delivery_amount" : "$25",
    "fast_delivery_days" : "1-2",
}

sellersDict = [
    {
        "id" : 1,
        "avatar" : user6,
        "name" : "Annette P. Kelsch",
        "store_name" : "Insulore",
        "products" : "485",
        "wallet_balance" : "$330,251",
        "create_date" : "09/05/2018",
        "revenue" : [25, 66, 30, 67, 33, 25, 34, 56, 65, 9, 54]
    },
    {
        "id" : 2,
        "avatar" : user1,
        "name" : "Timothy Kauper",
        "store_name" : "Uberer",
        "products" : "847",
        "wallet_balance" : "$258,125",
        "create_date" : "09/08/2018",
        "revenue" : [25, 66, 41, 34, 33, 25, 34, 50, 65, 9, 54]
    },
    {
        "id" : 3,
        "avatar" : user4,
        "name" : "Paul J. Friend",
        "store_name" : "Homovee",
        "products" : "128",
        "wallet_balance" : "$128,250",
        "create_date" : "07/07/2018",
        "revenue" : [25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54]
    },
    {
        "id" : 4,
        "avatar" : user3,
        "name" : "Kathryn S. Collier",
        "store_name" : "Epiloo",
        "products" : "78",
        "wallet_balance" : "$89,458",
        "create_date" : "06/30/2018",
        "revenue" : [25, 66, 41, 34, 63, 25, 34, 12, 434, 9, 54]
    },
    {
        "id" : 5,
        "avatar" : user3,
        "name" : "Bryan J. Luellen",
        "store_name" : "Execucy",
        "products" : "09",
        "wallet_balance" : "$78,410",
        "create_date" : "09/12/2018",
        "revenue" : [25, 66, 41, 45, 63, 25, 66, 12, 45, 9, 54]
    },
    {
        "id" : 6,
        "avatar" : user10,
        "name" : "Dean Smithies",
        "store_name" : "Circumous",
        "products" : "506",
        "wallet_balance" : "$68,143",
        "create_date" : "04/09/2018",
        "revenue" : [25, 82, 30, 67, 65, 25, 34, 56, 44, 9, 22]
    },
    {
        "id" : 7,
        "avatar" : user5,
        "name" : "Zara Raws",
        "store_name" : "Symic",
        "products" : "235",
        "wallet_balance" : "$56,210",
        "create_date" : "07/15/2018",
        "revenue" : [25, 66, 45, 34, 33, 34, 34, 50, 55, 9, 54]
    },
    {
        "id" : 8,
        "avatar" : user8,
        "name" : "Edward Roseby",
        "store_name" : "Hyperill",
        "products" : "77",
        "wallet_balance" : "$45,216",
        "create_date" : "08/23/2018",
        "revenue" : [25, 43, 30, 67, 34, 25, 34, 56, 43, 9, 56]
    },
    {
        "id" : 9,
        "avatar" : user1,
        "name" : "Labeeb Ghali",
        "store_name" : "Laudent",
        "products" : "121",
        "wallet_balance" : "$17,514",
        "create_date" : "06/19/2018",
        "revenue" : [25, 54, 30, 44, 65, 25, 34, 33, 44, 9, 23]
    },
    {
        "id" : 10,
        "avatar" : user2,
        "name" : "Rory Seekamp",
        "store_name" : "Centinte",
        "products" : "89",
        "wallet_balance" : "$14,384",
        "create_date" : "03/24/2018",
        "revenue" : [25, 82, 23, 67, 65, 67, 65, 56, 32, 19, 22]
    },
    {
        "id" : 11,
        "avatar" : user7,
        "name" : "Jenny C. Gero",
        "store_name" : "Susadmin",
        "products" : "38",
        "wallet_balance" : "$12,000",
        "create_date" : "08/02/2018",
        "revenue" : [25, 66, 30, 45, 33, 25, 44, 56, 33, 9, 33]
    },
    {
        "id" : 12,
        "avatar" : user9,
        "name" : "Anna Ciantar",
        "store_name" : "Vicedel",
        "products" : "347",
        "wallet_balance" : "$7,815",
        "create_date" : "05/06/2018",
        "revenue" : [25, 23, 30, 67, 34, 56, 34, 56, 85, 9, 56]
    },
]
