# Sprint 2 - A Minimum Viable Product (MVP)


## Sprint Goals

We need to develop a fully functional website that should implement all of the features that we need but doesn't need the same ui polish as where our refined Figma prototype was as this will come in sprint 3.


---

## Implemented Database Schema

Going into this sprint I also realised we need to add a location column to the activities table as we did not have this before.

![Schema with location as text](screenshots/schema_add_location.png)
Adding location does not affect any other columns so this is a simple change.

---

## Initial Implementation

The key functionality of the web app was implemented:

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE SYSTEM HERE**



During making the web app actually functional, I found that whenever I was using the first_name, I would likely be using last_name from my database as well. Due to this, I may as well as combine these two columns to make the schema simpler and handling the user names ever so slightly more simple and efficient

![Schema with name as text replacing first_name, last_name](screenshots/schema_add_location.png)





--- 


## Stakeholder feedback
I also gave this implementation to my stakeholders for them to give feedback on functionality only and they noticed the following

> How do we add and manage members?

I never gave this any thought as the members of the club hardly change so I was planning to update the database manually. 😅
Adding members manually and securely could be hard as passwords would have to be distribute 


---
## Our Testing
We will test the login functionality, logout, adding activities, adding resources, adding members, approving activities, removing activities and resources (committee) and removing members.


## Testing 

Replace this text with notes about what you are testing, how you tested it, and the outcome of the testing

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE TESTING HERE**

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE IMPROVED SYSTEM HERE**


---

## Testing Loading member only pages (profile, resources etc)

Logged in members should be able to access the pages but public should not.
![Navigating to various member pages](screenshots/member_pages_testing.gif)

We can see that members can load activities, profile, resources pages but when not logged in these pages are not available.

### Changes / Improvements
All functionality is present but some commented that the error page displayed when unauthorized users try to access a login_required page is not user friendly or consistent with the website.
As a result, we can make a specific unauthorised template that is shown in this case and could probably be used to give a specific error message when members are logged in but the fresh_login_required condition is not met.

![The new unauthorised error page](screenshots/member_pages_testing_2.gif)


---

## Testing Adding Activities

Members should be able to use the add activity form on the activities page to add a new activity to the specification that they wish
![Filling the new activity form and adding it](screenshots/add_activity_test.gif)

### Changes / Improvements

I had some difficulty with the current method of selecting activity datetime and to be sure I presented it to the committee and they queried why the date and time were in the same field. Separating the date and time could allow a nicer selection UI, especially using existing libraries in JS but the return that this provides is not worth the investment.

---

## Testing Adding Resources

Replace this text with notes about what you are testing, how you tested it, and the outcome of the testing

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE TESTING HERE**

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE IMPROVED SYSTEM HERE**


---

## Testing Approving Activity

Replace this text with notes about what you are testing, how you tested it, and the outcome of the testing

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE TESTING HERE**

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE IMPROVED SYSTEM HERE**




---


## Testing Approving Activity

Replace this text with notes about what you are testing, how you tested it, and the outcome of the testing

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE TESTING HERE**

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE IMPROVED SYSTEM HERE**



## Sprint Review

I am thankful that feedback given allowed me to implement adding members which would have probably detracted from key functionality.
