import React from 'react';
import {BrowserRouter as Router, Switch, Route, Link} from "react-router-dom";
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Drawer from '@mui/material/Drawer';
import { createTheme, ThemeProvider} from '@mui/material/styles';

import socket from './utils/websocket';
import RealtTime from './pages/Realtime';
import Scenarios from './pages/Scenarios';
import Simulation from './pages/Simulation'
import Home from './pages/home';

socket.on('connection', () => {
    console.log("connected");
  }
)

const App = () => {

  const theme = createTheme({
    palette: {
      mode: 'dark',
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Box sx={{ display: 'flex'}}>
            <Drawer variant="permanent" anchor="left" sx={{ width: 200, flexShrink: 0, '& .MuiDrawer-paper': {width: 200}}}>
              <Toolbar>
                <Typography> AirTrafficSim</Typography>
              </Toolbar>
              <Divider />
              <List>
                {/* <ListItemButton component={Link} to='/'>
                  <ListItemText primary={"Dashboard"} />
                </ListItemButton>
                <ListItemButton component={Link} to='/realtime'>
                  <ListItemText primary={"Real Time"}/>
                </ListItemButton> */}
                <ListItemButton component={Link} to='/replay'>
                  <ListItemText primary={"Replay"}/>
                </ListItemButton>
                <ListItemButton component={Link} to='/simulation'>
                  <ListItemText primary={"Simulation"}/>
                </ListItemButton>
              </List>
            </Drawer> 
          <Box component="main" sx={{ flexGrow: 1}}>
            <Switch>
              <Route path="/realtime" component={RealtTime}/>
              <Route path="/replay" component={Scenarios}/>
              <Route path="/simulation" component={Simulation}/>
              <Route path="/" exact component={Home}/>
            </Switch>  
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
