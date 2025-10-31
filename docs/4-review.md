# Project Review

## Addressing Relevant Implications

### Functionality Implications

I have rigorously tested this site throughout the design process to get to this point and I am proud that this website can be a useful tool for the branch. Club members are happy with the addition of the resources page to link valuable pieces of knowledge to the activity and they like that they are able to browse these separately.

### Usability Implications

I am happy with the usability of key areas of the site due to key design areas such as the activities system which are extremely easy to post and see due to being on the same page. I have also designed and ensured that the path from the home page to the contact us page is very easy to help meet the key requirement of it being easy for others to join the club. I have also compressed my site images from over 30mb as high quality photos to less than 10mb to reduce page loading times and increase server efficiency which will have a noticeable effect for loading times for a server application.

### Aesthetic Implications

I have done testing with the committee and the general public to establish a good colour scheme which makes the website friendly which the general public agrees with. I have also chosen my images well to make the website friendly again (see hamcram page). I am happy with the testing I have done to ensure my colours and site layout both looks and feels good from sprint 1 to now. 

### Privacy Implications

I believe I did well to address what I needed to ensure the users privacy. I believe using the werkzeug.security module with hashing and salting for password hashing is more than adequate to store the users passwords and I have also randomly generated the user passwords when their account is created for them which is a secure by default approach meaning there are no insecure passwords to be breached by default anyways. Crucially, this work cannot be wasted by a malicious actor reading the outgoing emails sent to users as not only are the users encouraged to change their passwords but the SMTP key I have provisioned is send only and stored securely in environment vars to continue to best align this project with industry best practices.

### Accessibility Implications

I have refined my semantic structure of my website to give screen readers and any other accessibility tools the best ability to navigate and use my site. I have made a conscious effort to separate roles of pages to try and balance clutter and cognitive load (ie separating activities and resources) to try and make the website make sense to all club members and public. As standard, I have also included *helpful* alt texts for all images I have used in the site which makes the website more enjoyable and welcoming to those with lower vision.

---

## Overall Review
I am very happy with how this project has progressed over time, especially during the stages of developing key functionality as I believe I have been able to support key functionality by adding key quality of life improvements such as the email system to add members easily which will promote the use of the system over time. However, the design phase in sprint 3 deserved some more work that I was unable to provide due to various reasons. If I were to do anything differently in the project, I would try and implement a more decentralised way of updating page content that makes it easy for club members to update any content in the about us page for example as outdated content is a problem in NZART Branch sites. (With github being too complex :P)

