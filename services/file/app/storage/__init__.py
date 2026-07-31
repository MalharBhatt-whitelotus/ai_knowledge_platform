"""
Here's the complete pseudocode for the Storage Abstraction layer.

 * Storage Provider Interface *
CLASS StorageProvider

    ABSTRACT FUNCTION save(file, filename)
        # Store the file
        # Return the storage path
    END FUNCTION


    ABSTRACT FUNCTION delete(path)
        # Delete the file from storage
    END FUNCTION


    ABSTRACT FUNCTION download(path)
        # Read the file from storage
        # Return the file contents
    END FUNCTION


    ABSTRACT FUNCTION exists(path)
        # Check whether the file exists
        # Return True or False
    END FUNCTION

END CLASS

* Local Storage Implementation *
CLASS LocalStorage EXTENDS StorageProvider

    FUNCTION initialize(upload_directory)
        STORE upload_directory
    END FUNCTION


    FUNCTION save(file, filename)

        CREATE destination_path

        CREATE upload directory IF it does not exist

        WRITE uploaded file TO destination_path

        RETURN destination_path

    END FUNCTION


    FUNCTION delete(path)

        IF file exists THEN

            DELETE file

        ELSE

            RAISE FileNotFound error

        END IF

    END FUNCTION


    FUNCTION download(path)

        IF file does not exist THEN

            RAISE FileNotFound error

        END IF

        READ file

        RETURN file contents

    END FUNCTION


    FUNCTION exists(path)

        IF file exists THEN
            RETURN True
        ELSE
            RETURN False
        END IF

    END FUNCTION

END CLASS

* Document Service Using Storage Abstraction *
CLASS DocumentService

    FUNCTION initialize(repository, storage_provider)

        STORE repository

        STORE storage_provider

    END FUNCTION


    FUNCTION upload_document(file)

        VALIDATE uploaded file

        GENERATE unique filename

        CALL storage_provider.save(file, filename)

        STORE returned storage path

        SAVE document information IN repository

        PUBLISH document event TO RabbitMQ

        RETURN uploaded document details

    END FUNCTION

END CLASS

* Upload Flow *
Receive Upload Request

        │
        ▼

Validate Uploaded File

        │
        ▼

Generate Unique Filename

        │
        ▼

Call StorageProvider.save()

        │
        ▼

Store File

        │
        ▼

Return Storage Path

        │
        ▼

Save Metadata in Database

        │
        ▼

Publish Processing Event

        │
        ▼

Return Success Response

* Delete Flow *
Receive Delete Request

        │
        ▼

Retrieve Document Information

        │
        ▼

Call StorageProvider.exists()

        │
        ▼

IF file does not exist

    RETURN File Not Found

END IF

        │
        ▼

Call StorageProvider.delete()

        │
        ▼

Delete Database Record

        │
        ▼

Return Success Response

* Download Flow *
Receive Download Request

        │
        ▼

Retrieve Storage Path

        │
        ▼

Call StorageProvider.exists()

        │
        ▼

IF file does not exist

    RETURN File Not Found

END IF

        │
        ▼

Call StorageProvider.download()

        │
        ▼

Return File to Client

* Future Storage Providers *
                Document Service
                       │
                       ▼
               Storage Provider
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
  Local Storage     S3 Storage    Azure Storage
        │              │              │
        ▼              ▼              ▼
 Local Files      Amazon S3      Azure Blob Storage

The key idea is that DocumentService never knows where the file is stored. It simply calls the methods defined by StorageProvider (save, delete, download, and exists), allowing you to switch storage backends (local disk, S3, MinIO, Azure Blob Storage, etc.) without modifying the service layer.
"""