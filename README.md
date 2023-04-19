## BLOGS QUERY

# get blog by id
query GetBlogById($id: Int = 1){
    blog(id: $id){
        name
        owner{
            username
            firstName
            lastName
            isStaff
            isSuperuser
            isActive
        }
        rating
        raters{
            id
            username
        }
    }
}

# get all blogs
query GetAllBlogs{
    blogs{
        name
        owner{
            username
            firstName
            lastName
            isStaff
            isSuperuser
            isActive
        }
        rating
        raters{
            id
            username
        }
    }
}

# get blogs by username only
query GetBlogByUsername($username: String = "mahtot"){
    blogs(username: $username){
        name
        owner{
            username
            firstName
            lastName
            isStaff
            isSuperuser
            isActive
        }
        rating
        raters{
            id
            username
        }
    }
}

# get blogs by there title
query GetBlogByTitle($title: String = "second"){
    blogs(title: $title){
        name
        owner{
            username
            firstName
            lastName
            isStaff
            isSuperuser
            isActive
        }
        rating
        raters{
            id
            username
        }
    }
}

# get all blogs of one user
query GetAllBlogsOfUser($user: Int = 1){
    user(id: $user){
        username
        firstName
        lastName
        blogSet{
            id
            name
            rating
            raters{
                id
                username
            }
        }
    }
}


## AUTHENTICATION

# get jwt token
mutation GetToken($username: String = "mahtot", $password: String = "mahtot mkonn"){
    tokenAuth(username: $username, password: $password){
        token
        payload
    }
}

# get refereshe token
mutation GetRefereshToken($token: String = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1haHRvdCIsImV4cCI6MTY4MjQ5NTczMiwib3JpZ0lhdCI6MTY4MTg5MDkzMn0.k59IZ-_HjrqSmAohElmqE1LIU7f2UCRsi8Awzj5TCv8"){
    refreshToken(token: $token){
        token
        refreshExpiresIn
        payload
    }
}

# get refereshe token
mutation VerifyToken($token: String = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1haHRvdCIsImV4cCI6MTY4MjQ5NTczMiwib3JpZ0lhdCI6MTY4MTg5MDkzMn0.k59IZ-_HjrqSmAohElmqE1LIU7f2UCRsi8Awzj5TCv8"){
    verifyToken(token: $token){
        payload
    }
}

## BLOGS MUTATION

# create blog
mutation CreateBlog($name: String = "my thired blog"){
    createBlog(name: $name){
        blog{
            id
            posts{
                content
                id
            }
            owner{
                username
                id
            }
        }
    }
}

# update blog
mutation UpdateBlog($id: Int = 1, $name: String = "my thired blog updateing"){
    updateBlog(name: $name, id: $id){
        blog{
            id
            name
            posts{
                content
                id
            }
            owner{
                username
                id
            }
        }
    }
}

# delete blog
mutation DeleteBlogById($id: Int = 1){
    deleteBlog(id: $id){
        message
    }
}


## COMMENTS QUERY

# get all comments
query GetAllComments{
    comments{
        id
        text
        createdDate
        user{
            username
            id
            isSuperuser
        }
        post{
            id
            title
            content
            pubDate
        }
    }
}

# get all comments of one user
query GetAllCommentsOfUser($id: Int = 1){
    user(id: $id){
        username
        comments{
            id
            text
            post{
                id
                content
                user{
                    id
                    username
                }
            }
        }
    }
}

# all likers of one post
query GetLikersOfPost($id: Int = 2){
    post(id: $id){
        id
        title
        content
        likes
        likers{
            id
            username
        }
    }
}

# all liked posts of user
query GetLikedPostsOfUser($id: Int = 1){
    user(id: $id){
        likedPosts{
            id
            title
            content
        }
    }
}

# all ratters of blog
query GetRatersOfBlog($id: Int = 2){
    blog(id: $id){
        name
        rating
        raters{
            username
            id
        }
    }
}
