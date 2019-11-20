import React from "react";
import styled from "styled-components";
import { FlatList, StyleSheet, Image, ScrollView, TouchableOpacity} from 'react-native';
import constants from "../../constants"
import { TouchableHighlight } from "react-native-gesture-handler";
import custom from "../../styles";

const View = styled.View`
    justify-content: center;
    align-items: center;
    flex: 1;
`;

const Text = styled.Text`
`;

onPress = () => {
  }

export default () => (
    <View style={styles.container}>
        <Text style={{fontSize:20, fontFamily: "Ys"}}>카테고리로 찾기</Text>


        <View style={styles.imageContainer}>
            <View style={styles.textWraper}>
                <TouchableHighlight onPress={this.onPress} underlayColor={custom.green}>
                    <Image source={{uri: "https://i.dlpng.com/static/png/455967_preview.png"}} 
                    style={styles.image}
                    />
                </TouchableHighlight>
            <Text style={styles.conponent_text}>과일</Text>
            </View>
            {/* </Box> */}

            {/* <Box> */}
            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "https://cdn.onlinewebfonts.com/svg/img_354378.png"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={styles.conponent_text}>채소</Text>
            </View>
            {/* </Box> */}

            {/* <Box> */}
            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "https://icon-library.net/images/rice-icon-png/rice-icon-png-1.jpg"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={styles.conponent_text}>쌀/잡곡</Text>
            </View>
            {/* </Box> */}

        </View>
        <View style={styles.imageContainer}>

            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQCyIWPgY0rsPlGczDDfTYQqLaL793dpCGNfg-K9EvOnwzvoe8I"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={styles.conponent_text}>정육/계란류</Text>
            </View>


            
            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQLmV8o-I5ISGe6d3Hjolt1FAo97kaSkPFUZlsETaDRW-iCnNZq"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={styles.conponent_text}>수산물/해산물</Text>
            </View>


            
            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTJAk_uRVCBXpwOtfn1N-428_hU2vsGhLZxVou1a58iys6bXO9-"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={styles.conponent_text}>유제품/냉장/냉동/간편식</Text>
            </View>
            
            

        </View>
        <View style={styles.imageContainer}>

            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRrkpT7d3fu7M2Xq6Tv28Vvt3hRBVBeKPyigZn1ramdGp_keURZ"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={styles.conponent_text}>과자/초콜릿/씨리얼/빵</Text>
            </View>



            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "https://data.silhouette-ac.com/data/thumbnails/80/803bc2413f8f6f351f0cef6b7d096a6b_t.jpeg"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={styles.conponent_text}>라면/통조림/조미료/장류</Text>
            </View>



            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTBnpoBoZiWe9q_QDiBleLlzXyfH96FlguJKnDWGRYkrnCKZGVm"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={styles.conponent_text}>음료/주류/커피/분유</Text>
            </View>


        </View>
        


    </View>
);

const styles = StyleSheet.create({
    container: {
        backgroundColor: "white",
        flex: 1,
        flexDirection: 'column',
        justifyContent: 'space-around',
        paddingTop:80,
        width: '100%',
        height: '10%',
    //    paddingBottom: 60

    },
    imageContainer:{
        flex: 1,
        width: constants.width,
        flexDirection: 'row',
        justifyContent: 'space-around',
    },

    image: {
        height: 100,
        width: 100,
        borderRadius: 30,
    },
    textWraper:{
        flexDirection: "column",
        width: 50,
        backgroundColor: "white"
    },
    conponent_text:{
        textAlign: "center",
        fontFamily: "Ys",
        fontSize: 14,
    }
})