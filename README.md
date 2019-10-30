# HackGT 6: MileSnap :zap::oncoming_automobile:

### In this project, our group aimed at creating an application that allows a user to take a picture of a gas station pricing sign and recieve the fuel type and its corresponding price for any type of sign, regardless of orientation or sign format. This was done using a combination of 2 separate cloud systems, 2 frameworks, and a custom-build API. :muscle: This tool could also be applied to other image recongition situations in the future with additional development. :globe_with_meridians:


## To do this, we've implemented the use of:
  ![Google](https://geekflare.com/wp-content/uploads/2018/06/cloud.google.png)
  ![AWS](https://res-3.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_120,w_120,f_auto,b_white,q_auto:eco/r4wsu8rl4jvpjydbhooy) 
  ![Flask](https://www.olirowan.xyz/static/images/icons/flask-plain.svg)
  ![React](https://img.icons8.com/ios/150/000000/react-native.png)
  * **The Google Cloud** :cloud:
    * Within the cloud, we chose to use the Google Vision API within the Vision AI module, which allows us to analyze any sign containing gas prices and return the fuel type and its corresponding price.
  * **AWS cloud** :cloud:
    * After passing the image through our custom API, the image and its corresponding HTTP link is stored on an AWS S3 Bucket, which then allows the API to pull the HTTP link safely and pass it to our image recognition API.
  * **Custom API using Flask** :outbox_tray:
    * Our custom built API takes the image passed from the interface and sends it to our AWS S3 Bucket. From there, the image is then requested back from the API and sent to the Google Vision API, which analyzes the image and returns the formatted fuel type/price list. This list is then sent through a JSON request by the UI to be displayed to the user.
  * **React Native** :iphone::computer:
    * This allows our interface to be compatible as an Android, iOS, and web app application, allowing for universal access across any device.

## How it works:

When the user opens the app, they will be prompted to select an image from their gallery that they would like to be analyzed. The user must crop their image to include **only** the desired fuel type and that fuel's price. This image is then taken by our custom API and is sent to a S3 AWS Bucket where the image is stored with a corresponding HTTP link that corresponds to where that image is stored on the AWS cloud.

This HTTP link is then requested by the API and sent to the Google Vision API to be analyzed for the prices and fuel types. Once the values are found, they are then sent to the UI on React Native via JSON request to be displayed on the screen for the user to see.

## Team:
@yashp121
@PranavPusarla
@computer-geek64
@therealsharath
