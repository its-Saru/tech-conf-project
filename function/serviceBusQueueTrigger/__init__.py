import logging
import azure.functions as func
import psycopg2
import os
import time
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    connect = psycopg2.connect(database="techconfdb",user="saruadmin@tech-conf-server",password="Thesalman101",host="tech-conf-server.postgres.database.azure.com")
    #postgresql://saruadmin@tech-conf-server:Thesalman101@tech-conf-server.postgres.database.azure.com/techconfdb
    cursor = connect.cursor()
    logging.info("Connection established")
 #cursor.execute('SELECT message,subject FROM notification WHERE id=%s;'.format(notification_id,))
    try:
        # TODO: Get notification message and subject from database using the notification_id
       
        cursor.execute('SELECT * FROM notification WHERE id = %s;', (notification_id,))
        notification = cursor.fetchone()
        
        # TODO: Get attendees email and name
        cursor.execute('SELECT first_name, last_name, email FROM attendee;')
        attendees = cursor.fetchall()

        # TODO: Loop through each attendee and send an email with a personalized subject
        for attendee in attendees:
          message = Mail(
              from_email='realdormat@gmail.com',
              to_emails=attendee[2],
              subject='{} {}'.format(attendee[1], notification),
              html_content=notification)
        try:
              sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
              response = sg.send(message)
              print(response.status_code,response.body,response.headers)
        except Exception as e:
            print(str(e))

        notificationDate = datetime.utcnow()
        notificationInfo = 'Notified {} attendees'.format(len(attendees))

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        cursor.execute('UPDATE notification SET status = %s, completed_date = %s WHERE id = %s;'.format(notificationInfo, notificationDate, notification_id))        
        connect.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        # TODO: Close connection
        cursor.close()
        connect.close()
        logging.info("Connection Closed")