import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

export default function DepartmentProductsPage() {
  const { id } = useParams();
  const [departmentName, setDepartmentName] = useState('');
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/departments/${id}/products`)
      .then(res => res.json())
      .then(data => {
        setDepartmentName(data.department || '');
        setProducts(data.products || []);
        setLoading(false);
      })
      .catch(() => {
        setDepartmentName('');
        setProducts([]);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div className="text-center py-10">Loading products...</div>;

  return (
    <div className="container mx-auto py-8 px-4">
      <Link to="/departments" className="text-blue-600 hover:underline mb-4 inline-block">
        &larr; Back to Departments
      </Link>
      <h1 className="text-3xl font-bold mb-6">{departmentName} Products</h1>

      {products.length === 0 ? (
        <p className="text-center text-gray-500">No products found in this department.</p>
      ) : (
        <div className="grid gap-8 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
          {products.map(product => (
            <Link
              to={`/products/${product.id}`}
              key={product.id}
              className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300"
            >
              <div className="h-48 bg-gray-200 flex items-center justify-center text-gray-400 text-3xl font-bold">
                {(product.name && product.name.length > 0) ? product.name[0].toUpperCase() : '?'}
              </div>
              <div className="p-4">
                <h2 className="text-lg font-semibold text-gray-900">{product.name || 'Unnamed Product'}</h2>
                <p className="text-gray-600 mb-1">{product.brand || 'Unknown Brand'}</p>
                <p className="text-indigo-600 font-bold text-xl">₹{product.retail_price || 'N/A'}</p>
                <p className="text-sm text-gray-400 mt-2">{product.category || 'Uncategorized'}</p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
