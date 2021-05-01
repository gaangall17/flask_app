from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import datetime

def write_new_alarms(rows):
    db_engine = create_engine('postgresql://geolib:FkGU59S6@localhost:5432/postgres')
    params = []
    for row in rows:
        params.append({
            "day": row[0],
            "full_name": row[1],
            "id": row[2], 
            "type": row[3],
            "count": row[4]
        })
    with db_engine.begin() as conn:
        conn.execute(
            text("""INSERT INTO public.alarms_count(day, full_name, id, alarm_type, count)
                    VALUES (:day, :full_name, :id, :type, :count)"""), 
            params
        )

def write_new_events(rows):
    db_engine = create_engine('postgresql://geolib:FkGU59S6@localhost:5432/postgres')
    params = []
    for row in rows:
        params.append({
            "date": row[0],
            "full_name": row[1],
            "id": row[2], 
            "type": row[3],
            "count": row[4]
        })
    with db_engine.begin() as conn:
        conn.execute(
            text("""INSERT INTO public.events_count(date, full_name, id, event_type, count)
                    VALUES (:date, :full_name, :id, :type, :count)"""), 
            params
        )