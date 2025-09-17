# Project Requirements

## Identified Problem or Need

Branch 26 needs a website! They need a way to advertise the hobby of amateur radio to the public and encourage interested people to join the club and for members to communicate the existence and details of various activities to the public and other members for advertising and coordination purposes.

## End-User Requirements

This site will have to cater to the general public and to the members of the club which have a wide demographic. There is a left skew in the age with many members being older men but most people who join are often younger and from a wider background. Some users are extremely tech savvy while others are not and this range will have to be considered in development. Members and the general public will likely access the site from mobile or desktop.

## Proposed Solution

The website will have a member login functionality that will restrict access to certain portions of the site (such as viewing member only activities or posting activities) to active club members. Activities should be able to be posted with different titles, descriptions and starting and ending dates (may run more than a day) and a member may have many activities posted at once. The club committee should be able to remove or edit details of any activity and to have some ability to edit the content of pages on the site.

---

# Relevant Implications

## Functionality Implications

Functionality implications are all about the website being able to perform it's intended duty *well*. (meaning no strange errors or bugs and the user can actually do what they wanted to)

### Relevance to the System

If the website does not work, it will not be adopted by members of the branch because the members will lose trust and patience with it working to inform them of the activities. This is particularly important as the site requires members to be active to post activities or else it will serve no use and it will definitely not be used. 

### Impact / Considerations

I will test each part of the functionality of the system to make sure it works, and it works consistently in a way that the user expects. I need to test enough functionality to ensure that the users will be happy (viewing, posting and approving activities, adding and viewing resources etc as well as ensuring the public facing section of the website is attractive to non-members). Testing should cover all ranges and types of inputs.


## Usability Implications

Usability is about how easy it is for the user to do the task that they wanted without pulling their hair out. If functionality is about if things are possible to perform then usability is about how easy and clear to understand the actions needed to perform them are.

### Relevance to the System

This site, ideally deployed, should become a regular part of club life as the club constantly have activities. It is not good enough that the website is possible to use, it should nice for members to use otherwise they won't use it anyway.

### Impact / Considerations

I can always do my best to try and improve usability as I improve functionality but ultimately user trialing and stakeholder feedback will allow me to best improve usability. I should also follow Neilson's usability heuristics during the design process especially consistency and standards, flexibility and efficiency etc.


## Aesthetic Implications

Aesthetic implications are all about whether the website actually looks okay (or not). If the users like how it looks, and conventions are met such as readable fonts and matching colors with design features like alignment repetition etc then the aesthetics are a success.

### Relevance to the System

It is important to have good aesthetics for this project especially as the public facing section of the website will be the non-members first impressions of the club so if we want to make a good impression to convince them to join the site should look the part.

### Impact / Considerations

I am not the best graphic designer so getting good feedback from the branch committee is essential to identify what looks good and what does not, which can hopefully allow me then to change what has to be changed and make it look like what does look good until the website looks okay. What I can do is follow best practices when designing including selecting good colour, fonts and layout according to principles such as colour harmonies, structure, repetition, contrast etc.


## Privacy Implications

Privacy Implications are about making sure that your user's data is held and processed safely and securely in your site. To meet them, you should try to collect as little data about your users as possible and ensuring what you do collect is properly secure and held to NZ privacy laws.

### Relevance to the System

The members of branch 26 will have some data held on the website such as callsign and password for login and email and phone number as well as name for contacting them. This needs to be held and processed/served at a level of moderate security (as high as reasonable) as this is a lot of data that can be used to identify people. We also want to keep their passwords as safe as possible.

### Impact / Considerations

- When storing the user's secured info in our database we can perform password hashing to ensure that no-one that gets access to the database (me included) can see the member's passwords which may be used in other places which would compromise their security. 
- We can use obfuscation tools when displaying our designated contacts info to prevent web crawlers harvesting it.
- Inform users during onboarding that their personal information will be handled to be transparent (also saying what information)

## Accessibility Implications

Accessibility Implications are all about making sure that all users can use the site even if they have compromised abilities or are on an unconventional device. Therefore, we need to ensure that we cater for those with impaired vision (color blindness, dyslexia etc) or those using the site one handed on mobile or even with assistance such as a screen reader.

### Relevance to the System

There are a lot of elderly members in the club and the website should also be able to be used by the general public so we *will* have to cater for these users with various needs.

### Impact / Considerations

We can follow accessibility best practices such as using alt text and ensuring proper HTML hierarchy for compatibility with screen readers. We can also do testing on elements such as text to ensure that contrast is appropriate for those with impaired vision. Ensuring good design choices such as good fonts and sizing is also important for clarity and usability for all.


## End-User Implications

End-user implications are about meeting the users specific needs for using the site. This means that they can get what they came to do done, while catering to their expectations and case requirements (such as multi-platform device support). If they are happy and feel catered for / included then you have met the End-User implications.

### Relevance to the System

It is important to meet what the members (and general public) need from the branch website or else they will not want to engage with the website at all which will result in it becoming useless if no activities would be posted.

### Impact / Considerations

I know that the demographic of members is extremely diverse and that members will want to use the site on a range of devices so we should ensure that we cater for this. Checking in with the committee for feedback also helps here as they will know their various needs that I need to cater to better and we can use this to develop the website accordingly.