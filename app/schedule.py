from datetime import datetime, timedelta

from database.models import Reminders


async def check_reminders():
    now = datetime.now()

    reminders = await Reminders.filter(total_date__lte=now).prefetch_related("user")

    for reminder in reminders:
        await send_notification(reminder.user.tg_id, reminder.text)

        reminder.total_date = reminder.total_date + timedelta(days=180)
        
        await reminder.save()
