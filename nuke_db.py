from awards import db, models, create_app

if __name__ == '__main__':
    if input('Are you sure you want to nuke all the tables in the database from space? (y/N) ') == 'y':
        app = create_app()
        app.app_context().push()
        models.Student.query.delete()
        models.Awards.query.delete()
        models.AwardRecipients.query.delete()
        db.session.commit()
        print('Done!')
    else:
        print('Canceled!')
        
