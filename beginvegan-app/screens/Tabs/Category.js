import React from "react";
import styled from "styled-components";
import { FlatList, StyleSheet, Image, ScrollView, TouchableOpacity} from 'react-native';
import constants from "../../constants"

const View = styled.View`
    justify-content: center;
    align-items: center;
    flex: 1;
`;

const Text = styled.Text`
`;

export default () => (
    <View style={styles.container}>
        <Text style={{fontSize:17}}>카테고리로 찾기</Text>
        <View style={styles.imageContainer}>


            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "https://www.scienceall.com/nas/image/201204/EMB00000a180d33.bmp"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={{textAlign: "center"}}>과일</Text>
            </View>


            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "https://t1.daumcdn.net/liveboard/realfood/4c6470eb049343a89c61067316b9bc58.JPG"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={{textAlign: "center"}}>채소</Text>
            </View>



            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "http://t1.daumcdn.net/liveboard/realfood/2fefb77f548848e7aba646058fa8bc12.JPG"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={{textAlign: "center"}}>쌀/잡곡</Text>
            </View>


        </View>
        <View style={styles.imageContainer}>

            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "http://gdimg.gmarket.co.kr/755102972/still/600?ver=0"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={{textAlign: "center"}}>정육/계란류</Text>
            </View>


            
            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "http://gohyangfood.com/data/item/1423401192_m"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={{textAlign: "center"}}>수산물/해산물</Text>
            </View>


            
            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "https://previews.123rf.com/images/baibaz/baibaz1603/baibaz160300046/55868581-%EB%AA%A9%EC%A1%B0-%EB%B0%B0%EA%B2%BD%EC%97%90-%EB%8B%A4%EC%96%91-%ED%95%9C-%EC%8B%A0%EC%84%A0%ED%95%9C-%EC%9C%A0%EC%A0%9C%ED%92%88.jpg"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={{textAlign: "center"}}>유제품/냉장/냉동/간편식</Text>
            </View>
            
            

        </View>
        <View style={styles.imageContainer}>

            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "http://img.danawa.com/prod_img/500000/085/731/img/7731085_1.jpg?shrink=500:500&_v=20190417135418"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={{textAlign: "center"}}>과자/초콜릿/씨리얼/빵</Text>
            </View>



            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "http://img.vogue.co.kr/vogue/2018/01/style_5a55dc28c936c.jpg"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={{textAlign: "center"}}>라면/통조림/조미료/장류</Text>
            </View>



            <View style={styles.textWraper}>
            <TouchableOpacity>
            <Image source={{uri: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbOtRlUAExUyg8y69ioBI720ZWXg_1-3PNu3hfUszh4pma0STM"}} 
            style={styles.image}
            />
            </TouchableOpacity>
            <Text style={{textAlign: "center"}}>음료/주류/커피/분유</Text>
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
        paddingBottom: 60
    },
    imageContainer:{
        flex: 1,
        width: constants.width,
        flexDirection: 'row',
        justifyContent: 'space-around',
    },
    imageContainerTop:{
        flex: 1,
        width: constants.width,
        flexDirection: 'row',
        justifyContent: 'space-around'
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
    }
})