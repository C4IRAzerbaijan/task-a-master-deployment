# Vercel File System Error Fix - Complete Setup Guide

## The Problem

When deploying to Vercel, you get this error:
```
[Errno 30] Read-only file system: 'documents'
```

This occurs because **Vercel's file system is read-only**. Only `/tmp` is writable, but it's ephemeral (cleared after each request). This breaks document uploads and the RAG system.

## Solution: Vercel Blob Storage

We've implemented support for **Vercel Blob Storage** - a persistent file storage service built into Vercel.

### What Changed

1. **New Blob Storage Service** (`services/blob_storage_service.py`)
   - Handles uploads to Vercel Blob Storage
   - Fallback to local filesystem for development
   - Automatic detection of Vercel environment

2. **Updated Database** (`utils/database.py`)
   - Added `is_blob_storage` column to track storage type
   - Can handle both local and blob-stored files

3. **Enhanced RAG Service** (`services/enhanced_rag_service.py`)
   - Added `process_document_from_bytes()` method
   - Allows processing files downloaded from blob storage

4. **Updated Upload Handler** (`backend/simple_app.py`)
   - Automatically uses Blob Storage on Vercel
   - Falls back to local filesystem in development
   - Handles both download and deletion from blob storage

## Setup Instructions

### Step 1: Create Vercel Blob Storage Token

1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Navigate to your project
3. Go to **Settings → Storage**
4. Click **Create Database** → **Blob**
5. Name it (e.g., "documents-storage")
6. Copy the token that appears

### Step 2: Set Environment Variable on Vercel

1. In your Vercel project settings:
   - Go to **Settings → Environment Variables**
   - Add new variable:
     - **Name:** `VERCEL_BLOB_TOKEN`
     - **Value:** Paste the token from Step 1
     - **Environments:** Production, Preview, Development

2. Redeploy your application

### Step 3: Deploy Updated Code

```bash
# Push the new code to your repository
git add -A
git commit -m "Add Vercel Blob Storage support for document uploads"
git push origin main

# (Your CI/CD will automatically deploy to Vercel)
```

### Step 4: Test Upload

1. Go to your deployed application
2. Log in with admin account
3. Try uploading a document
4. Check that it processes successfully

## How It Works

###  Local Development (No Blob Storage Needed)

```
Document Upload
    ↓
Detect Environment (not Vercel)
    ↓
Save to Local ./documents/ Folder
    ↓
Process with RAG Service
```

### Vercel Production

```
Document Upload
    ↓
Detect Environment (IS Vercel)
    ↓
Check for VERCEL_BLOB_TOKEN
    ↓
Upload to Vercel Blob Storage
    ↓
Store Blob URL in Database
    ↓
Download File Content for RAG Processing
    ↓
Process with RAG Service
```

## Environment Detection

The code automatically detects the Vercel environment:

```python
is_vercel = os.getenv('VERCEL', '') == '1'  # Set automatically by Vercel

if is_vercel and blob_storage.blob_enabled:
    # Use Vercel Blob Storage
else:
    # Use local filesystem
```

## Testing the Fix

### Test 1: Upload Document
1. Admin login
2. Upload a PDF/Word/Text document
3. Should see: "Fayl uğurla yükləndi və işləndi"

### Test 2: View Documents
1. Go to Documents section
2. Should see uploaded document with status "Processed"

### Test 3: Chat with Document
1. Select the document
2. Ask a question
3. Should get answers from the document

### Test 4: Download Document
1. Click download on any document
2. File should download successfully

## Troubleshooting

### Error: "Blob storage not configured"

**Solution:** 
- Verify `VERCEL_BLOB_TOKEN` environment variable is set
- Check Vercel dashboard → Project Settings → Environment Variables
- Redeploy after adding the variable

### Error: "Blob upload failed"

**Solution:**
- Check that Blob Storage is created in your Vercel project
- Verify token is correct and not expired
- Check network connectivity

### Error: "File not found on download"

**Solution:**
- Ensure document was uploaded successfully
- Check that `is_blob_storage` column was added to database
- May need to re-upload documents

## Database Schema Update

The documents table now includes:

```sql
ALTER TABLE documents ADD COLUMN is_blob_storage BOOLEAN DEFAULT FALSE;
```

This column tracks whether a document is stored in:
- Blob Storage (`TRUE`) - for Vercel production
- Local filesystem (`FALSE`) - for development or pre-update documents

## Files Modified/Created

- ✅ **Created**: `services/blob_storage_service.py` - New blob storage handler
- ✅ **Updated**: `utils/database.py` - Added `is_blob_storage` column
- ✅ **Updated**: `services/enhanced_rag_service.py` - Added byte processing
- ✅ **Updated**: `backend/simple_app.py` - Updated upload/download/delete handlers
- ✅ **Updated**: `routes/document_routes.py` - Alternative route handlers (for reference)

## Key Features

- ✅ **Automatic Environment Detection** - Works on Vercel and Local
- ✅ **Persistent Storage** - Files survive request cycles
- ✅ **Fallback Support** - Works without blob token (local dev)
- ✅ **Database tracking** - Knows which storage type each file uses
- ✅ **Seamless Processing** - RAG service handles both storage types
- ✅ **Delete Support** - Can delete files from blob storage or local
- ✅ **Download Support** - Streaming downloads from blob storage

## Next Steps

1. Set up Vercel Blob Storage token (see Step 1)
2. Add `VERCEL_BLOB_TOKEN` to environment variables
3. Deploy the updated code
4. Test document upload
5. If issues persist, check error logs in Vercel dashboard

## Additional Resources

- [Vercel Blob Documentation](https://vercel.com/docs/storage/vercel-blob)
- [Vercel Environment Variables](https://vercel.com/docs/projects/environment-variables)
- [Flask File Uploads](https://flask.palletsprojects.com/uploading-files/)

## Support

If you encounter issues:
1. Check Vercel deployment logs
2. Verify `VERCEL_BLOB_TOKEN` is set correctly
3. Run local test first (without blob token)
4. Check database has `is_blob_storage` column
