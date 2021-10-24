import React from 'react';
import {BrowserRouter as Router, Switch, Route, Link} from "react-router-dom";

import Home from './pages/home'
import Cesium from './pages/cesium';

import './App.css';
import logo from './logo.svg';

const App = () => {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">home</Link>
            </li>
            <li>
              <Link to="/cesium">cesium</Link>
            </li>
          </ul>
        </nav>

        <Switch>
          <Route path="/cesium">
            <Cesium/>
          </Route>
          <Route path="/">
            <Home/>
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
