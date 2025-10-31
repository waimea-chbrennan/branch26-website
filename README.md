# Nelson Amateur Radio Club (NZART Branch 26) Website

by Connor Brennan 


---

## Project Description

Nelson Amateur Radio Club (referred to as B26/ Branch 26) needs a public facing website to promote the hobby of amateur radio to the public, giving them the opportunity to join the club. Members should be able to post activities to the site with some being private to confirmed members while others should be able to post important activities to be public.

- Sign in area for members.
- Members only page allowing posting and viewing of "small" activities.
- Prominent members can post large official club meetings that are open to the public.
- Showcase of amateur radio to the public (ie historic activities) that make the hobby look appealing.
- Strong call to action to for public to join *our* club. 


---

## Project Links

- [GitHub repo for the project](https://github.com/waimea-chbrennan/branch26-website)
- [Project Documentation](https://waimea-chbrennan.github.io/branch26-website/)
- [Live web app](https://branch26-website.onrender.com)

**Credentials for moderation**

Primary Callsign: `ZL4MODR`

Password: `fl3xb0x-h34d4ch3-xx`
Replace xx with the year. Security, Eh?

---

## Project Files

- Program source code can be found in the [app](app/) folder
- Project documentation is in the [docs](docs/) folder, including:
   - [Project requirements](docs/0-requirements.md)
   - Development sprints:
      - [Sprint 1](docs/1-sprint-1-prototype.md) - Development of a prototype
      - [Sprint 2](docs/2-sprint-2-mvp.md) - Development of a minimum viable product (MVP)
      - [Sprint 3](docs/3-sprint-3-refinement.md) - Final refinements
   - [Final review](docs/4-review.md)
   - [Setup guide](docs/setup.md) - Project and hosting setup

---

## Project Details

This is a digital media and database project for **NCEA Level 2**, assessed against standards [91892](docs/as91892.pdf) and [91893](docs/as91892.pdf).

The project is a web app that uses [Flask](https://flask.palletsprojects.com) for the server back-end, connecting to a SQLite database. The final deployment of the app is on [Render](https://render.com/) with a placeholder database held there as well.

The app uses [Jinja2](https://jinja.palletsprojects.com/templates/) templating for structuring pages and data, and [PicoCSS](https://picocss.com/) as the starting point for styling the web front-end.

The project demonstrates a number of **advanced database techniques**:
- Linking data in related tables or nodes using queries or keys
- Writing custom queries to filter and/or sort data
- Using logical, mathematical and/or wildcard operators
- Customising presentation of the data
- Using custom forms to add user input to the database
- Setting validation rules for data entry

The project demonstrates a number of **advanced digital media (web) techniques**:
- Creating or customising scripts, code or presets
- Using a combination of steps to manipulate or enhance elements
- Using a third-party library
- Using composite effects



