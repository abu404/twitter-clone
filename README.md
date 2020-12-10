# twitter-clone
Simple Twitter clone to post tweet, follow and un follow users etc

>Step 1: Create a Docker Volume
```
docker volume create
```
>Step 2: Run the follwoing command to run the project
```
docker-compose up --build
```
>Step 3: Wait till both MySQL and Django app is up


#####Sometimes the mysql can take sometime to launch. Since the app runs in parallel with db,
the app could crash till the db is up. This is intentional, please give 5 min to the services to up. 
####
<br>

>Step 4: Navigate to the following URL
```
http://localhost:6001/
```

#####The above url hosts the swagger ui. 


##API'S
##### There are two sets of APIs. One for authentication and other is the twiiter APIs

>Login

```
POST
​/auth​/login
Sample Request Body
{
    "username": "abutahir",
    "password": "test1"

}
```
> Register 
```
POST
​/auth​/register
Sample Request Body
{
    "email" : "abu@gmail.com",
    "password": "test1",
    "first_name": "abu",
    "last_name": "tahir",
    "username": "abutahir"
}
```
>######Note : Login endpoint returns a access token which has to be set while making calls to twitter api.

>##Create a Tweet
```
POST
/v1/twitter/tweet
Sample Request Body
{
  "content": "string",
  "is_retweet": true
}
```
* #####The tweet gets added mapped to authenticated user.

>##Like a Tweet
* The url takes the tweet id in the url and takes user_id in request body
* The user can be any valid user
```
PUT
/v1/twitter/tweet/like/{id}
{
    "user_id" : 0
}
```
>##Unlike a Tweet
* The url takes the tweet id in the url and takes user_id in request body
* The user can be any valid user
```
PUT
/v1/twitter/tweet/unlike/{id}
{
    "user_id" : 0
}
```

>##Follow a user
* The url takes the tweet id in the url and takes user_id in request body
* The user can be any valid user
```
POST
/v1/twitter/user/follow
{
    "user_id" : 0
}
```
* The user_id can be any valid user_id. Since there is any constraints given a user can follow himself.
* However this can be handled with minimal code change.

>##Unfollow a user
* The user can be any valid user
```
POST
/v1/twitter/user/unfollow
{
    "user_id" : 0
}
```

>##Get User's followings
```
POST
/v1/twitter/user/following
```

>##Get Tweet's likers
```
POST
/v1/twitter/tweet/likes/{id}
```
* Takes Tweet id in the URL




