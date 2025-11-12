import { useState } from 'react';
import { useAuth } from '@/features/auth/context';
import { Link } from 'react-router-dom';

export const Register = () => {
  const [formData, setFormData] = useState({
    login: '',
    firstName: '',
    lastName: '',
    password: '',
  });
  const [errors, setErrors] = useState({
    login: '',
    firstName: '',
    lastName: '',
    password: '',
  });
  const { register, isLoading, error } = useAuth();

  const validateField = (name: string, value: string) => {
    let errorMessage = '';
    
    if (!value.trim()) {
      errorMessage = 'This field is required';
    } else {
      switch (name) {
        case 'login':
          if (value.length < 3) {
            errorMessage = 'Login must be at least 3 characters';
          } else if (!/^[a-zA-Z0-9_]+$/.test(value)) {
            errorMessage = 'Login can only contain letters, numbers, and underscores';
          }
          break;
        case 'firstName':
        case 'lastName':
          if (value.length < 2) {
            errorMessage = 'Name must be at least 2 characters';
          }
          break;
        case 'password':
          if (value.length < 6) {
            errorMessage = 'Password must be at least 6 characters';
          }
          break;
      }
    }
    
    return errorMessage;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setErrors(prev => ({ ...prev, [name]: validateField(name, value) }));
  };

  const isFormValid = () => {
    const newErrors = {
      login: validateField('login', formData.login),
      firstName: validateField('firstName', formData.firstName),
      lastName: validateField('lastName', formData.lastName),
      password: validateField('password', formData.password),
    };
    
    setErrors(newErrors);
    return Object.values(newErrors).every(error => error === '');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (isFormValid()) {
      await register(
        formData.login,
        formData.firstName,
        formData.lastName,
        formData.password
      );
    }
  };

  return (
    <div className="flex min-h-screen flex-col justify-center px-6 py-12 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-sm">
        <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
          Create your account
        </h2>
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form className="space-y-6" onSubmit={handleSubmit}>
          {(error || Object.values(errors).some(e => e)) && (
            <div className="rounded-md bg-red-50 p-4 text-sm text-red-800">
              {error && <p>{error}</p>}
              {!error && Object.values(errors).filter(e => e).map((e, i) => <p key={i}>{e}</p>)}
            </div>
          )}
          
          <div>
            <label htmlFor="login" className="block text-sm font-medium leading-6 text-gray-900">
              Login
            </label>
            <div className="mt-2">
              <input
                id="login"
                name="login"
                type="text"
                required
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3"
                value={formData.login}
                onChange={handleChange}
                disabled={isLoading}
              />
              {errors.login && <p className="mt-1 text-sm text-red-600">{errors.login}</p>}
            </div>
          </div>

          <div>
            <label htmlFor="firstName" className="block text-sm font-medium leading-6 text-gray-900">
              First Name
            </label>
            <div className="mt-2">
              <input
                id="firstName"
                name="firstName"
                type="text"
                required
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3"
                value={formData.firstName}
                onChange={handleChange}
                disabled={isLoading}
              />
              {errors.firstName && <p className="mt-1 text-sm text-red-600">{errors.firstName}</p>}
            </div>
          </div>

          <div>
            <label htmlFor="lastName" className="block text-sm font-medium leading-6 text-gray-900">
              Last Name
            </label>
            <div className="mt-2">
              <input
                id="lastName"
                name="lastName"
                type="text"
                required
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3"
                value={formData.lastName}
                onChange={handleChange}
                disabled={isLoading}
              />
              {errors.lastName && <p className="mt-1 text-sm text-red-600">{errors.lastName}</p>}
            </div>
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium leading-6 text-gray-900">
              Password
            </label>
            <div className="mt-2">
              <input
                id="password"
                name="password"
                type="password"
                required
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3"
                value={formData.password}
                onChange={handleChange}
                disabled={isLoading}
              />
              {errors.password && <p className="mt-1 text-sm text-red-600">{errors.password}</p>}
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={isLoading}
            >
              {isLoading ? 'Creating account...' : 'Create account'}
            </button>
          </div>
        </form>

        <p className="mt-10 text-center text-sm text-gray-500">
          Already have an account?{' '}
          <Link
            to="/login"
            className="font-semibold leading-6 text-indigo-600 hover:text-indigo-500"
          >
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
};