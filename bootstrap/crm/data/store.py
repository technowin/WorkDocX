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


# dashboard 
statisticsCRMDict = {
    "CampaignSent" : {
        "number": "9,184",
        "per": "3.27%",
        "arrow": "up",
    },
    "NewLeads" : {
        "number": "3,254",
        "per": "5.38%",
        "arrow": "down",
    },
    "Deals" : {
        "number": "861",
        "per": "4.87%",
        "arrow": "up",
    },
    "BookedRevenue" : {
        "number": "$253k",
        "per": "11.7%",
        "arrow": "up",
    },
}

revenueStatCRMDist = {
    "current_month": "$42,025",
    "previous_month": "$74,651",
}

topPerformingDict = [
    {"user": "Jeremy Young", "role": "Senior Sales Executive",
        "leads": "187", "Deals": "154", "tasks": "49"},
    {"user": "Thomas Krueger", "role": "Senior Sales Executive",
        "leads": "235", "Deals": "127", "tasks": "83"},
    {"user": "Pete Burdine", "role": "Senior Sales Executive",
        "leads": "365", "Deals": "148", "tasks": "62"},
    {"user": "Mary Nelson", "role": "Senior Sales Executive",
        "leads": "753", "Deals": "159", "tasks": "258"},
    {"user": "Kevin Grove", "role": "Senior Sales Executive",
        "leads": "458", "Deals": "126", "tasks": "73"},
]

recentLeadsStatusDict = {
    "cold_lead": {"name": "Cold lead", "color": "warning"},
    "lost_lead": {"name": "Lost lead", "color": "danger"},
    "won_lead": {"name": "Won lead", "color": "success"}
}

recentLeadsDict = [
    {"avatar": user2, "name": "Risa Pearson", "email": "richard.john@mail.com",
        "status": recentLeadsStatusDict["cold_lead"]},
    {"avatar": user3, "name": "Margaret D. Evans", "email": "margaret.evans@rhyta.com",
        "status": recentLeadsStatusDict["lost_lead"]},
    {"avatar": user4, "name": "Bryan J. Luellen", "email": "bryuellen@dayrep.com",
        "status": recentLeadsStatusDict["won_lead"]},
    {"avatar": user5, "name": "Kathryn S. Collier", "email": "collier@jourrapide.com",
        "status": recentLeadsStatusDict["cold_lead"]},
    {"avatar": user1, "name": "Timothy Kauper", "email": "thykauper@rhyta.com",
        "status": recentLeadsStatusDict["cold_lead"]},
    {"avatar": user6, "name": "Zara Raws", "email": "austin@dayrep.com",
        "status": recentLeadsStatusDict["won_lead"]},
]


# project
projectSummary = [
    {"name" : "Project Discssion" , "des":"6 Person" , "icon" :"account-group" , "color" : "primary"},
    {"name" : "In Progress" , "des":"16 Projects" , "icon" :"progress-pencil" , "color" : "warning"},
    {"name" : "Completed Projects" , "des":"24" , "icon" : "checkbox-marked-circle-outline" , "color" : "danger"},
    {"name" : "Delivery Projects" , "des":"20" , "icon" :"send" , "color" : "success"},
]

projectDescription = [
    {"name" : "Active Project" , "count":"85" , "icon":"file-document-edit" , "color":"primary"},
    {"name" : "Total Employees" , "count":"32", "icon":"account-group" , "color":"success"},
    {"name" : "Project Review" , "count":"40", "icon":"account-star" , "color":"info"},
    {"name" : "New Project" , "count":"25", "icon":"folder-plus" , "color":"warning"}
]

projectOverview = [
    {"name":"Product Design" , "projects":"26" , "employee" : "4" , "color":"primary"},
    {"name":"Web Development" , "projects":"30" , "employee" : "5" ,  "color":"danger"},
    {"name":"Illustration Design" , "projects":"12" , "employee" : "3" ,  "color":"success"},
    {"name":"UI/UX Design" , "projects":"8" , "employee" : "4" ,  "color":"warning"}
]

dailyTask = [
    {"name" : "Landing Page Design" , "des" : "Create a new landing page (Saas Product)" , "people" : "5" , "hour" :"2"},
    {"name" : "Admin Dashboard" , "des" : "Create a new Admin dashboard" , "people" : "2" , "hour" :"3"},
    {"name" : "Client Work" , "des" : "Create a new Power Project (Sktech design)" , "people" : "2" , "hour" :"5"},
    {"name" : "UI/UX Design" , "des" : "Create a new UI Kit in figma" , "people" : "3" , "hour" :"6"}
]

teamMembers = [
    {"avatar":user2, "name":"Risa Pearson" ,"designation":"UI/UX Designer" , "experience":"2.5 Year Experience" },
    {"avatar":user3, "name":"Margaret D. Evans" ,"designation":"PHP Developer" , "experience":"2 Year Experience" },
    {"avatar":user4, "name":"Bryan J. Luellen" ,"designation":"Front end Developer" , "experience":"1 Year Experience" },
    {"avatar":user5, "name":"Kathryn S. Collier" ,"designation":"UI/UX Designer" , "experience":"1 Year Experience" },
    {"avatar":user1, "name":"Timothy Kauper" ,"designation":"Backend Developer" , "experience":"3 Year Experience" },
    {"avatar":user6, "name":"Zara Raws" ,"designation":"Python Developer" , "experience":"2 Year Experience" }
]


# order list 
orderStatus = {
    "in_progress" :{"name" : "In Progress" , "color" : "info"},
    "complete" :{"name" : "Complete" , "color" : "success"},
    "pending" :{"name" : "Pending" , "color" : "warning"},
    "delivered" :{"name" : "Delivered" , "color" : "primary"}
}

ordersList = [
    {"id" : "#CM9708" , "customer_name" : "Jerry Geiger" ,"customer_image": user1 , "project" : "Landing Page" ,"city" : "New York", "address" : "Meadow Lane Oakland" , "date" : "01 January 2022" , "status" : orderStatus["in_progress"]},
    {"id" : "#CM9707" , "customer_name" : "Adam Thomas" ,"customer_image":user2 , "project" : "Client Project (Sktech)" ,"city" : "Canada", "address" : "Bagwell Avenue Ocala" , "date" : "02 January 2022" , "status" : orderStatus["complete"]},
    {"id" : "#CM9706" , "customer_name" : "Sara Lewis" ,"customer_image":user3 , "project" : "Admin Dashboard" ,"city" : "Denmark", "address" : "Washburn Baton Rouge" , "date" : "03 January 2022" , "status" : orderStatus["pending"]},
    {"id" : "#CM9705" , "customer_name" : "Myrtle Johnson" ,"customer_image":user4 , "project" : "Landing Page (Figma)" ,"city" : "Brazil", "address" : "Nest Lane Olivette" , "date" : "04 January 2022" , "status" : orderStatus["delivered"]},
    {"id" : "#CM9704" , "customer_name" : "Bryan Collier" ,"customer_image":user5 , "project" : "App Landing Page" ,"city" : "Mexico", "address" : "Larry San Francisco" , "date" : "05 January 2022" , "status" : orderStatus["in_progress"]},
    {"id" : "#CM9703" , "customer_name" : "Joshua Moody" ,"customer_image":user6 , "project" : "CRM Admin pages" ,"city" : "Russia", "address" : "Oak Drive Mobile" , "date" : "06 January 2022" , "status" : orderStatus["complete"]},
    {"id" : "#CM9702" , "customer_name" : "John Clune" ,"customer_image":user7 , "project" : "Ecommerce Dashboard" ,"city" : "Manitoba", "address" : "Oxford Court Amory" , "date" : "07 January 2022" , "status" : orderStatus["delivered"]},
    {"id" : "#CM9701" , "customer_name" : "Jamie Romero" ,"customer_image":user8 , "project" : "Logo Design" ,"city" : "Nova Scotia", "address" : "Lane New Market" , "date" : "08 January 2022" , "status" : orderStatus["pending"]},
    {"id" : "#CM9700" , "customer_name" : "Clint Percival" ,"customer_image":user9 , "project" : "PHP Project" ,"city" : "Manitoba", "address" : "Wilson Avenue Dallas" , "date" : "09 January 2022" , "status" : orderStatus["delivered"]},
    {"id" : "#CM9699" , "customer_name" : "Donna Lynch" ,"customer_image":user10 , "project" : "Landing Section" ,"city" : "Yukon", "address" : "Avenue Johnson City" , "date" : "10 January 2022" , "status" : orderStatus["complete"]}
    
]

# clients 
clientsList = [
    {"name" : "Louise Coleman ", "icon":"true","url":"LouiseMColeman@dayrep.com", "avatar" : user1, "projects":"18"},
    {"name" : "Robert Kent" ,"icon":"true","url":"RobertSKent@jourrapide.com", "avatar" : user2, "projects":"24"},
    {"name" : "Arthur Childress" ,"icon":"false","url":"ArthurEChildress@teleworm.us", "avatar" : user3, "projects":"11"},
    {"name" : "Ronald McGehee " ,"icon":"true","url":"RonaldHMcGehee@jourrapide.com", "avatar" : user4, "projects":"06"},
    {"name" : "Martin Jordan" ,"icon":"true","url":"MartinDJordan@armyspy.com", "avatar" : user5, "projects":"12"},
    {"name" : "Dewayne Murphy" ,"icon":"false","url":"DewayneBMurphy@armyspy.com", "avatar" : user6, "projects":"15"},
    {"name" : "Russel Sanchez" ,"icon":"true","url":"RusselHSanchez@rhyta.com", "avatar" : user7, "projects":"22"},
    {"name" : "Alvin Middleton" ,"url":"AlvinSMiddleton@armyspy.com", "avatar" : user8, "projects":"07"}
]

# management 
clients = [
    {"name" :"Kevin Snowden" , "des" :"Simple Solutions LLC" , "date" :"Jan 05 2022" , "avatar":user1 },
    {"name" :"Steven Embry" , "des" :"Flipside Records LLC" , "date" :"Jan 10 2022" , "avatar":user2},
    {"name" :"James McDonald" , "des" :"Vision Clinics LLC" , "date" :"Jan 12 2022" , "avatar":user3},
    {"name" :"Ralph Wolford" , "des" :"Merry-Go-Round LLC" , "date" :"Jan 18 2022" , "avatar":user5},
    {"name" :"Tomas Cooper" , "des" :"Museum LLC" , "date" :"Feb 02 2022" , "avatar":user6}
]

status_data = {
    "in_progress":{"name":"In Progress","color":"primary"},
    "completed":{"name":"Completed","color":"success"},
    "pending":{"name":"Pending","color":"warning"}
}

monthlyProgress = [
    {"name" : "Adam Baldwin" , "avatar": user1 ,"email" :"AdamNBaldwin@dayrep.com" , "project":"Admin Dashboard", "status":status_data["in_progress"]},
    {"name" : "Peter Wallace" , "avatar": user2,"email" :"PeterGWallace@dayrep.com" , "project":"Landing Page", "status":status_data["completed"]},
    {"name" : "Jacob Dunn" , "avatar": user3,"email" :"JacobEDunn@dayrep.com" , "project":"Logo Design", "status":status_data["pending"]},
    {"name" : "Terry Adams" , "avatar": user4,"email" :"TerryCAdams@dayrep.com" , "project":"Client Project", "status":status_data["in_progress"]},
    {"name" : "Jason Stovall" , "avatar": user5,"email" :"JasonJStovall@armyspy.com" , "project":"Figma Work", "status":status_data["pending"]}
]

task_status = [

]