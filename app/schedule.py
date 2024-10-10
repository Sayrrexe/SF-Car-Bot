from datetime import datetime, timedelta

from app.database.models import Reminders, User


async def check_reminders():
    from run import bot

    now = datetime.now()

    reminders = await Reminders.filter(total_date__lte=now).prefetch_related("user")

    for reminder in reminders:
        await bot.send_message(reminder.user.tg_id, reminder.text)

        reminder.total_date = now + (reminder.total_date - reminder.created_at)
        await reminder.save()


async def send_seasonal_notifications():
    from run import bot

    users = await User.all()
    for user in users:
        await bot.send_message(user.tg_id, "Время поменять омывайку и шины")
