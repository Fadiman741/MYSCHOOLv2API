MYSCHOOLAPI: Comprehensive Educational Platform API


The MYSCHOOLAPI is a robust Django REST Framework (DRF)-based API that powers an educational platform, integrating PostgreSQL for data storage and Cloudinary for media management. It facilitates grade-based subject discussions, social interactions (posts, comments, replies, likes), tutor discovery, and institution-specific content creation with rich media support.

Core Features & Implementation

1. User Roles & Authentication

✅ The system supports four distinct user roles:

    Students – Can join grade-subject discussions, interact with posts, and search for tutors.

    Teachers – Can moderate discussions, create posts, and manage subject content.

    Tutors – Can offer tutoring services, be discovered via search, and engage in discussions.

    Institutions – Can publish articles with custom styling and media attachments.

2. Grade-Subject Management (Admin)

  ✅ Admins can:

    Add grades (e.g., Grade 10, Grade 11).

    Assign subjects (e.g., Mathematics, Physics) to each grade.

    Each grade-subject pair acts as a discussion room.

3. Discussion System (Posts, Comments, Replies, Likes)

✅ Users can:

    Create posts in subject-specific rooms.

    Comment on posts.

    Reply to comments.

    Like posts, comments, or replies.

    Attach images/videos (via Cloudinary).

4. Tutor Discovery System

✅ Students can:

    Search tutors by subject, experience, or location.

    View tutor profiles (bio, ratings, availability).


5. Institution Articles (Rich Content)

✅ Institutions can:

    Create articles with custom styling.

    Embed images/videos (Cloudinary integration).



Technical Stack

Component	Technology Used

✅ Backend	: Django REST Framework

✅ Database	: PostgreSQL (scalable, relational)

✅ Media Storage	: Cloudinary (image/video uploads)

✅ Authentication :	Token-based (JWT optional)

✅ Search	: Django-filter, PostgreSQL full-text search

✅ Deployment	: Docker, AWS/GCP, Nginx




Conclusion

The MYSCHOOLAPI is a role-based educational platform that enables:

✅ Grade-subject discussions (like virtual classrooms)

✅ Social interactions (posts, comments, likes)

✅ Tutor discovery (search by subject/location)

✅ Institution publishing (rich media articles)    
