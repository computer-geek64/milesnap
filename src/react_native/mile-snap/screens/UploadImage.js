import * as React from 'react';
import { Button, Text, View} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import Constants from 'expo-constants';
import * as Permissions from 'expo-permissions';

export default class ImagePickerExample extends React.Component {
    
    state = {
        image: null,
        tes: 'No image uploaded',
    }
    
    render() {
      let { tes } = this.state;
  
      return (
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <Text>{'\n'}</Text>
        <Button
          style = {{fontSize: 20, size: 20, marginTop: 50}}
          color="#05ff00"
          title="SNAP"
          onPress={this._pickImage}
        />
          {tes !== '' && 
            <Text style={{color: '#05ff00', fontSize: 17, margin: 30, marginTop: 10,}}>
                {"\n"}{ tes }
            </Text>}
        </View>
      );
    }
  
    componentDidMount() {
      this.getPermissionAsync();
    }
  
    getPermissionAsync = async () => {
      if (Constants.platform.ios) {
        const { status } = await Permissions.askAsync(Permissions.CAMERA_ROLL);
        if (status !== 'granted') {
          alert('Sorry, we need camera roll permissions to make this work!');
        }
      }
    }

    _pickImage = async () => {
        let result = await ImagePicker.launchImageLibraryAsync({
          mediaTypes: ImagePicker.MediaTypeOptions.All,
          allowsEditing: true,
        });
    
        console.log(result);
    
        if (!result.cancelled) {
            this.setState({ image: result.uri });   
            const data = new FormData();
            fileExtension = result.uri.substring(result.uri.length-3, result.uri.length);
    
            data.append('image', {
                uri: result.uri,
                name: `photo.${fileExtension}`,
                type: `image/${fileExtension}`,
            });
    
            fetch("http://143.215.60.53:81/milesnap/api/v1.0/upload?token=jepho9aeik63hei6", {
                method: "POST",
                headers: {
                    "Content-Type": "multipart/form-data",
                },
                body: data,
            }) .then(response => {
                return response.json();
            }) .then(res => {
                    var result = 'Prices Detected from your image';
                    result += '\n';
                    for (var key in res) {
                        if (res.hasOwnProperty(key)) {
                            console.log(key + res[key])
                            result += key + ": " + res[key] + '\n';
                        }
                    this.setState({ tes: result});
                    }
            }) .catch(function(error) {
                console.log('There has been a problem: ' + error.message);
                throw error;
            })
        }
    }
}