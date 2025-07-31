import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

export default function DepartmentProductsPage() {
  const { id } = useParams();
  const [department, setDepartment] = useState('');
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/departments/${id}/products`)
      .then(res => res.json())
      .then(data => {
        setDepartment(data.department || '');
        setProducts(data.products || []);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div className="text-center py-10">Loading...</div>;
  return (
    <div className="container mx-auto py-8 px-4">
      <Link to="/departments" className="text-blue-700 hover:underline">&larr; All Departments</Link>
      <h2 className="text-2xl font-bold mb-6">{department} Department ({products.length} products)</h2>
      {products.length === 0 ? (
        <div className="text-gray-500">No products found in this department.</div>
      ) : (
        <div className="grid gap-8 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
          {products.map(product => (
            <Link to={`/products/${product.id}`} key={product.id}
                  className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300">
              <div className="h-48 bg-gray-200 flex items-center justify-center
                              text-gray-400 text-3xl font-bold">
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
