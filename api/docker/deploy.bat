heroku login
heroku container:login

:: "getaround-api-qg2022" should be replaced with your app's name
heroku container:push web -a getaround-api-qg2022

:: "getaround-api-qg2022" should be replaced with your app's name
heroku container:release web -a getaround-api-qg2022

:: "getaround-api-qg2022" should be replaced with your app's name
:: access doc: https://getaround-api-qg2022.herokuapp.com/docs
heroku open -a getaround-api-qg2022

pause