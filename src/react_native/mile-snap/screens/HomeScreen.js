import * as WebBrowser from 'expo-web-browser';
import React from 'react';
import UploadImage from './UploadImage';
import {
  Image,
  ScrollView,
  StyleSheet,
  Text,
  View,
  Button,
} from 'react-native';

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.contentContainer}>
        <View style={styles.welcomeContainer}>
          <Image
              source={require('../assets/images/icon.png')}
              style={styles.welcomeImage}
          />
        </View>

        <View style={styles.getStartedContainer}>
          <Text style={styles.developmentModeText}>
              Leverage the power of machine learning to capture information about gas prices
          </Text>
          <UploadImage payloadKey='image' // Field name
            endpoint='http://143.215.60.53:81/milesnap/api/v1.0/upload?token=testing'
            callbackUrl={'../assets/images/mainLogo.png'} // CallBack Image url
            style={styles.developmentModeText}
          />
          <Text style={styles.developmentModeText}>
            Projects done for HackGT 6: "Into the Rabbit Hole" by team Biriyani Bandits
          </Text>
          <Text style={{color: '#fff', fontSize: 17, margin: 30, marginTop: 10,}}>
            Ashish D'Souza{"\n"}
            Pranav Pusarla{"\n"}
            Yash Patel{"\n"}
            Sharath Palathingal{"\n"}
          </Text>
        </View>
      </ScrollView>
    </View>
  );
}

HomeScreen.navigationOptions = {
  header: null,
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    alignContent: 'center',
  },
  developmentModeText: {
    margin: 10,
    maxWidth: 400,
    color: '#fff',
    fontSize: 17,
    lineHeight: 19,
    textAlign: 'center',
  },
  contentContainer: {
    paddingTop: 30,
    textAlign: "center",
  },
  welcomeContainer: {
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 20,
  },
  welcomeImage: {
    width: 100,
    height: 100,
    resizeMode: 'contain',
    marginTop: 3,
    marginLeft: -10,
  },
  homeScreenFilename: {
    marginVertical: 7,
  },
  codeHighlightText: {
    color: 'rgba(96,100,109, 0.8)',
  },
  getStartedText: {
    fontSize: 17,
    color: '#fff',
    lineHeight: 24,
    textAlign: 'center',
  },
  
  navigationFilename: {
    marginTop: 5,
  },
  helpContainer: {
    marginTop: 15,
    alignItems: 'center',
  },
  helpLink: {
    paddingVertical: 15,
  },
  helpLinkText: {
    fontSize: 14,
    color: '#2e78b7',
  },
});