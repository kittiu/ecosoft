Enable the "Update Restrict Model" of specific model to restrict update from unpermitted users.
To set a user as a permitted user to update restricted model(s), click on "Unrestrict
Update" toggle button in the user form.

Optionally, to set a user as read-only user to all models, click on "Read-only" toggle
button in the user form.

Read-only users can still open wizards (transient models), e.g. report wizards, so
they can print reports. Changes to real documents remain blocked. Note that a wizard
which writes data using ``sudo()`` is not blocked, so do not give read-only users
the access group of such wizards.
