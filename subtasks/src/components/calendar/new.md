# Drag complete process

 Basically we should have daypanels completely devoid of logic, (just as
 background), but with date highlighting like we have now (they should probably
 have parent goals in the header still though.

Then we have a component generate the panels/panel (with the day of the week) on the header if day/week view.

After that we have a component add all timeslots to the screen with margins dynamically generated from their dates. then they will just live on top of the panels.

On drag since we have the size of the daypanel we can use that as a locking mechanism (+= etc). we can keep the up down process, we just have to make sure that it stays in the div

# Considerations

for the month view our logic might need to be different and annoying to lock correctly, probably look at what gcal does to see if they actually support resizing sections

new event process

I think we should let the day panels control the creation of events, and emit them to the parent. I think in v1 we should not support multi-day-spanning events. (which does lock us out of importing gcal calendars but that I think is fine for now)

