Requirements
------------

- Users can load a pre-provided schedule and save to their account
- Loading schedule includes loading rules around panels
    - Travel time between rooms
    - Ticket pick-up window

- Use LightBox as initial case
- Automatic integration with planning APIs of conferences
- Automatic ingestion of conference schedules


Schemas
-------

- Conference
    - Name
    - Location
    - Dates

- Room
    - Conference
    - Location
    - Capacity
    - Presenter

- Attendee
    - Name
    - Username
    - Password

- Presenter
    - Name
    - Website

- Panel
    - Room
    - Start Time
    - End Time

- Presenter >--< Panel
- Attendee >--< Panel
- Attendee >--< Conference

