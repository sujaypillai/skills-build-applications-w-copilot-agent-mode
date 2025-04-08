from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        try:
            # Connect to MongoDB
            logger.debug("Connecting to MongoDB...")
            client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
            db = client[settings.DATABASES['default']['NAME']]
            logger.debug(f"Database name: {settings.DATABASES['default']['NAME']}")
            logger.debug(f"Host: {settings.DATABASES['default']['HOST']}, Port: {settings.DATABASES['default']['PORT']}")

            # Drop existing collections
            logger.debug("Dropping existing collections...")
            db.users.drop()
            db.teams.drop()
            db.activity.drop()
            db.leaderboard.drop()
            db.workouts.drop()
            logger.debug(f"Collections after drop: {db.list_collection_names()}")

            # Create users
            logger.debug("Creating users...")
            users = [
                User(_id=ObjectId(), username='thundergod', email='thundergod@mhigh.edu', password='thundergodpassword'),
                User(_id=ObjectId(), username='metalgeek', email='metalgeek@mhigh.edu', password='metalgeekpassword'),
                User(_id=ObjectId(), username='zerocool', email='zerocool@mhigh.edu', password='zerocoolpassword'),
                User(_id=ObjectId(), username='crashoverride', email='crashoverride@hmhigh.edu', password='crashoverridepassword'),
                User(_id=ObjectId(), username='sleeptoken', email='sleeptoken@mhigh.edu', password='sleeptokenpassword'),
            ]
            User.objects.bulk_create(users)

            # Log user creation
            logger.debug(f"Users created: {users}")
            logger.debug(f"Inserted users: {list(db.users.find())}")

            # Create teams
            logger.debug("Creating teams...")
            team = Team(_id=ObjectId(), name='Blue Team')
            team.save()
            team.members.add(*users)

            # Log team creation
            logger.debug(f"Team created: {team}")
            logger.debug(f"Inserted teams: {list(db.teams.find())}")

            # Create activities
            logger.debug("Creating activities...")
            activities = [
                Activity(_id=ObjectId(), user=users[0], activity_type='Cycling', duration=timedelta(hours=1)),
                Activity(_id=ObjectId(), user=users[1], activity_type='Crossfit', duration=timedelta(hours=2)),
                Activity(_id=ObjectId(), user=users[2], activity_type='Running', duration=timedelta(hours=1, minutes=30)),
                Activity(_id=ObjectId(), user=users[3], activity_type='Strength', duration=timedelta(minutes=30)),
                Activity(_id=ObjectId(), user=users[4], activity_type='Swimming', duration=timedelta(hours=1, minutes=15)),
            ]
            Activity.objects.bulk_create(activities)

            # Log activity creation
            logger.debug(f"Activities created: {activities}")
            logger.debug(f"Inserted activities: {list(db.activity.find())}")

            # Create leaderboard entries
            logger.debug("Creating leaderboard entries...")
            leaderboard_entries = [
                Leaderboard(_id=ObjectId(), user=users[0], score=100),
                Leaderboard(_id=ObjectId(), user=users[1], score=90),
                Leaderboard(_id=ObjectId(), user=users[2], score=95),
                Leaderboard(_id=ObjectId(), user=users[3], score=85),
                Leaderboard(_id=ObjectId(), user=users[4], score=80),
            ]
            Leaderboard.objects.bulk_create(leaderboard_entries)

            # Log leaderboard creation
            logger.debug(f"Leaderboard entries created: {leaderboard_entries}")
            logger.debug(f"Inserted leaderboard entries: {list(db.leaderboard.find())}")

            # Create workouts
            logger.debug("Creating workouts...")
            workouts = [
                Workout(_id=ObjectId(), name='Cycling Training', description='Training for a road cycling event'),
                Workout(_id=ObjectId(), name='Crossfit', description='Training for a crossfit competition'),
                Workout(_id=ObjectId(), name='Running Training', description='Training for a marathon'),
                Workout(_id=ObjectId(), name='Strength Training', description='Training for strength'),
                Workout(_id=ObjectId(), name='Swimming Training', description='Training for a swimming competition'),
            ]
            Workout.objects.bulk_create(workouts)

            # Log workout creation
            logger.debug(f"Workouts created: {workouts}")
            logger.debug(f"Inserted workouts: {list(db.workouts.find())}")

            self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise