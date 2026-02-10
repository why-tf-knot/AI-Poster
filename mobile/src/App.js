import React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {createStackNavigator} from '@react-navigation/stack';
import HomeScreen from './screens/HomeScreen';
import FeaturesScreen from './screens/FeaturesScreen';
import AboutScreen from './screens/AboutScreen';

const Stack = createStackNavigator();

const App = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: {
            backgroundColor: '#000000',
          },
          headerTintColor: '#ffffff',
          headerTitleStyle: {
            fontWeight: 'bold',
            fontSize: 20,
            letterSpacing: 2,
          },
        }}>
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{title: 'AI-POSTER'}}
        />
        <Stack.Screen
          name="Features"
          component={FeaturesScreen}
          options={{title: 'FEATURES'}}
        />
        <Stack.Screen
          name="About"
          component={AboutScreen}
          options={{title: 'ABOUT'}}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;
