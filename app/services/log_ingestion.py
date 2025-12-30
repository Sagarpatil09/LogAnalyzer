import os

from app.models.directory import Directory
from app.models.log_entry import LogEntry
from app.models.log_file import LogFile
from app.utils.parser import parse_log_line


def ingest_logs(directory_path: str, db):
    """Ingest log files from the specified directory into the database."""
    try:
        directory = db.query(Directory).filter_by(path=directory_path).first()
        if directory:
            return {"message": "Directory already processed"}

        directory = Directory(path=directory_path)
        db.add(directory)
        db.commit()
        db.refresh(directory)

        for filename in os.listdir(directory_path):
            if os.path.splitext(filename)[1] not in {".log", ".txt"}:
                continue

            file_path = os.path.join(directory_path, filename)

            log_file = LogFile(filename=filename, directory_id=directory.id)
            db.add(log_file)
            db.commit()
            db.refresh(log_file)

            with open(file_path, "r") as f:
                for line in f:
                    parsed = parse_log_line(line)
                    if not parsed:
                        continue

                    log_entry = LogEntry(**parsed, file_id=log_file.id)
                    db.add(log_entry)

            db.commit()

        return {"message": "Logs ingested successfully"}
    
    except HTTPException:
        db.rollback()
        raise

    except (OSError, IOError) as file_error:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"File system error: {str(file_error)}"
        )

    except SQLAlchemyError as db_error:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while ingesting logs"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )