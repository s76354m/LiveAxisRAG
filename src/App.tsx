import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ThemeProvider } from '@mui/material';
import { Layout } from './components/Layout';
import { ProjectList } from './pages/projects/ProjectList';
import { ProjectDetails } from './pages/projects/ProjectDetails';
import { theme } from './theme';

const queryClient = new QueryClient();

export const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <BrowserRouter>
          <Layout>
            <Routes>
              <Route path="/" element={<ProjectList />} />
              <Route path="/projects/:id" element={<ProjectDetails />} />
            </Routes>
          </Layout>
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  );
}; 