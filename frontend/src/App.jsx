import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ProductsPage from './pages/ProductsPage';
import ProductDetailPage from './pages/ProductDetailPage';
import DepartmentsPage from './pages/DepartmentsPage';
import DepartmentProductsPage from './pages/DepartmentProductsPage';

export default function App() {
  return (
    <BrowserRouter>
      {/* Optionally add Header component here */}
      <Routes>
        <Route path="/" element={<ProductsPage />} />
        <Route path="/products/:id" element={<ProductDetailPage />} />
        <Route path="/departments" element={<DepartmentsPage />} />
        <Route path="/departments/:id" element={<DepartmentProductsPage />} />
      </Routes>
      {/* Optionally add Footer component here */}
    </BrowserRouter>
  );
}
