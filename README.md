## Image server

This is a Web app for uploading public images. Developers can use the API to upload images, and the backend is built with FastAPI. The app has the following features:

Dynamic thumbnail creation: Thumbnails of uploaded images are created automatically to reduce the load time of the page.
Image caching technique: Uploaded images are cached on the server to improve performance and reduce server load.

## Getting Started

To get started with the app, follow these steps:

git clone <repository-url> 
```
 cd frontend
 npm install
 npm start 
 open http://localhost:3000
 
```

```
cd backend
pip install -r requirements.txt
python main.py

```

## Usage

The app provides an easy-to-use interface for uploading images. Developers can also use the API to upload images programmatically. Here are the details:

## Uploading Images

To upload an image using the app, follow these steps:

Click the "Upload Image" button.
Select an image from your computer.
Enter a title for the image.
Click the "Upload" button.
The app will upload the image to the server, and a thumbnail of the image will be displayed on the page.

Using the API

Developers can use the API to upload images programmatically. Here are the details:

> POST /image/upload-image

Request Body

The request body should contain the following fields:

file: The image file to upload.

Example
Here's an example of how to upload an image using the API:

> fetch('/image/upload-image',{Authorization:'Bearer ${key}'} {
  method: 'POST',
  body: new FormData().append('file', file),
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});


- [x] Dynamic thumbnail creation
- [x] Image caching :tada:
- [ ] Multiple Image uploading
- [ ] progress bar
- [ ] Signup Link
