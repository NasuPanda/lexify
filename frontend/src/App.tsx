import type { FC } from 'react';
import './App.css';

console.log(import.meta.env.VITE_APP_TITLE);
console.dir(import.meta.env);

const App: FC = () => (
  <>
    <h1>Hello, RailsAPi and React by Docker</h1>
  </>
);

export default App;
