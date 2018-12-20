Running
1. Start Flask’s built-in web server (with pethealth/):
        flask run
2. Visit the URL outputted by flask to see the web application.

Registration and Log In
Since each user inputs indifferent data, it is thus crucial to have a user registration system that allows us to keep track of individualized information. Also, for the purpose of privacy protection, logging in with username and password is crucial for data access.
The user must make an account to begin using Petty. To do so, start by pressing the “Register” button in the top right corner.
Input unique username, email address, and password.
1. Confirm the password, making sure that it matches the initial combination inputted.
2. Once successfully registered, log in by pressing the “Log In” button in the top right corner.

Log Diet and Exercise
The purpose of our web application is to reflect user’s physical health through pet health. The health status of the pet changes depending on the user’s diet and level of activity. To do so, we ask the user to manually input their meals and workouts:
1. To log meals, the user simply press on the “Diet” tab to start off.
2. Once in the page, the user records the food item consumed.
3. Then, using nutrition labels, the user records the amounts of calories, fat, and sugar in what they ate.
4. Similarly, to log exercise, the user enters the “Exercise” page using the corresponding tab.
5. Then, we ask the user to record the activity performed as well as the duration of exercise.
6. Once the information is inputted, the user sees either a happy (healthy), in-between, or sad (unhealthy) corgi. The image reflects the user’s health status. The goal is to motivate healthy living via pet care.

Goal Helper
This part of our web application suggests different workouts depending on the user’s target health level.
1. The user sets a goal by first clicking the “Goal” tab on the top.
2. Depending on the level of ambition, we recommend different workouts for users. For example, for one looking for a high health level (>  180), we recommend high-intensity workouts such as Barry’s Bootcamp.
Note: Our goal was to have default values in the Google Maps search depending on the level of intensity. While we were able to redirect the user to different pages, each with a Google Maps search, depending on the value inputted, we were unable to have default values in the search box. This is one aspect of our project that we want to improve on with additional resources. Also, because we solidified this function after recording our video, it is not include in our walk-through.

Survey
We further include a survey for the user to complete to receive recommendations of health-improving facilities that fit an individual’s lifestyle. We were able to implement the survey page for the user to fill out, which we use to calculate a wellness score that we use to map out locations (i.e. restaurants and gyms) that can assist with lifestyle changes. We, however, have a bug that prevents the user from submitting the form.  This part of our project is thus something that we would like to complete if given more time and resources.