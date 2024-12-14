import os

def create_file(file_path, content):
    """Creates a file with the given content."""
    with open(file_path, 'w') as file:
        file.write(content)

def create_folders(folders):
    """Creates the folder structure."""
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

def create_files(files):
    """Creates the files with specified content."""
    for file_path, content in files.items():
        create_file(file_path, content)

# Prompt for the project name
project_name = input("Enter the project name: ")

# Define the folder structure
folders = [
    f"{project_name}/app",
]

# Define the file structure with content
files = {
    f"{project_name}/app/__init__.py": """from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from .exts import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .auth import auth_ns

def create_app(config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)
    db.init_app(app)
    Migrate(app, db)
    api = Api(app, doc='/docs')
    api.add_namespace(auth_ns)
    JWTManager(app)
    return app
""",
    f"{project_name}/app/auth.py": """from flask_restx import Resource, Namespace, fields
from flask import request, jsonify
from .models import User
from .exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

auth_ns = Namespace('auth', description="A namespace for authentication")

signup_model = auth_ns.model(
    "User",
    {
        "id": fields.Integer(),
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String()
    }
)

signin_model = auth_ns.model(
    "User",
    {
        "username": fields.String(),
        "password": fields.String()
    }
)

@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        db_user = User.query.filter_by(username=username).first()
        if db_user is not None:
            return jsonify({"message": f"User with username {username} already exists"})
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password'))
        )
        new_user.save()
        return jsonify({"message": "Signup Success"})

@auth_ns.route('/signin')
class SignIn(Resource):
    @auth_ns.expect(signin_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        db_user = User.query.filter_by(username=username).first()
        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)
            return jsonify({
                "access_token": access_token,
                "refresh_token": refresh_token
            })
        else:
            return jsonify({"message": "User not found"})
""",
    f"{project_name}/app/models.py": """from .exts import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()
""",
    f"{project_name}/app/exts.py": """from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
""",
    f"{project_name}/config.py": """from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, 'dev.db')
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProdConfig(Config):
    pass

class TestConfig(Config):
    pass
""",
    f"{project_name}/manage.py": """from flask.cli import FlaskGroup
from app import create_app, db
from flask_migrate import Migrate

app = create_app('config.DevConfig')
migrate = Migrate(app, db)
cli = FlaskGroup(create_app=lambda:app)

if __name__ == '__main__':
    cli()
""",
    f"{project_name}/run.py": """from app import create_app
from config import DevConfig

if __name__ == '__main__':
    app = create_app(DevConfig)
    app.run()
""",
    f"{project_name}/wsgi.py": """from app import create_app
from config import DevConfig

if __name__ == '__main__':
    app = create_app(DevConfig)
    app.run()
""",
    f"{project_name}/requirements.txt": """Flask
flask-restx
flask-sqlalchemy
flask-migrate
flask-jwt-extended
python-decouple
python-dotenv
pywin32
fcntl
gunicorn
Flask-CORS
werkzeug""",
    f"{project_name}/.env": """SECRET_KEY=586dfe9c5a2bfe48ae0781fe
SQLALCHEMY_TRACK_MODIFICATIONS=False
""",
    f"{project_name}/.gitignore": """
# Python cache
__pycache__/
*.py[cod]
*$py.class

# virtual environment
venv/
*.pyc

# Flask specific settings
instance/

# Logs
*.log

# DB files
*.sqlite3
*.db

# IDE-specific files
*.suo
*.swp
*.swo
*.swi
*.pyo
*.pyw
.idea/
*.sublime-project
*.sublime-workspace
.env

# Node modules
node_modules/

# Package manager files
pipenv/
Pipfile.lock
*.egg-info/

""",
   f"{project_name}/readMe.md": """
    # Authentication API Integration with Axios in React TypeScript

## Setup

### 1. Install Dependencies
```bash
npm install axios react-router-dom @types/react-router-dom
```

### 2. Create Authentication Types
```typescript
// src/types/auth.ts
export interface SignupCredentials {
  username: string;
  email: string;
  password: string;
}

export interface SigninCredentials {
  username: string;
  password: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
}
```

### 3. Create Authentication Service
```typescript
// src/services/authService.ts
import axios from 'axios';
import { SignupCredentials, SigninCredentials, AuthTokens } from '../types/auth';

const BASE_URL = 'http://your-backend-url/api/auth';

export const authService = {
  async signup(credentials: SignupCredentials): Promise<{ message: string }> {
    try {
      const response = await axios.post(`${BASE_URL}/signup`, credentials);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async signin(credentials: SigninCredentials): Promise<AuthTokens> {
    try {
      const response = await axios.post(`${BASE_URL}/signin`, credentials);
      
      // Store tokens in local storage
      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
      }

      return response.data;
    } catch (error) {
      throw error;
    }
  },

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }
};
```

### 4. Create Authentication Context
```typescript
// src/context/AuthContext.tsx
import React, { createContext, useState, useContext, ReactNode } from 'react';
import { authService } from '../services/authService';

interface AuthContextType {
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  signup: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(
    !!localStorage.getItem('access_token')
  );

  const login = async (username: string, password: string) => {
    try {
      await authService.signin({ username, password });
      setIsAuthenticated(true);
    } catch (error) {
      setIsAuthenticated(false);
      throw error;
    }
  };

  const signup = async (username: string, email: string, password: string) => {
    try {
      await authService.signup({ username, email, password });
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    authService.logout();
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
```

### 5. Create Protected Route Component
```typescript
// src/components/ProtectedRoute.tsx
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};
```

### 6. Example Login and Signup Components
```typescript
// src/pages/LoginPage.tsx
import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(username, password);
      navigate('/dashboard');
    } catch (error) {
      console.error('Login failed', error);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button type="submit">Login</button>
    </form>
  );
};

// Similar structure for SignupPage
```

### 7. Axios Interceptor for Token Management
```typescript
// src/services/axiosConfig.ts
import axios from 'axios';
import { authService } from './authService';

axios.interceptors.request.use(
  (config) => {
    const token = authService.getAccessToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Optional: Refresh token logic can be added here
```

## Usage in App
```typescript
// src/App.tsx
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
```

## Key Considerations
- Securely store tokens in `localStorage`
- Implement proper error handling
- Use environment variables for API URLs
- Consider implementing token refresh mechanism
- Add form validation
- Implement proper loading and error states in components
""",

}

# Execute folder and file creation
create_folders(folders)
create_files(files)

print(f"Flask project '{project_name}' has been initialized successfully.")
print("")
# Instructions for running the project
print("\nTo run the project, follow these steps:")
print("1. Navigate to the project directory: cd " + project_name)
print("2. Create a virtual environment: python -m venv venv")
print("3. Activate the virtual environment:")
print("   On Windows: venv\\Scripts\\activate")
print("   On Mac/Linux: source venv/bin/activate")
print("4. Install dependencies: pip install -r requirements.txt")
print("5. Run migrations to set up the database:")
print("   a. Initialize migrations: python manage.py db init")
print("   b. Generate migration scripts: python manage.py db migrate -m 'Initial migration'")
print("   c. Apply migrations: python manage.py db upgrade")
print("6. Run the application: python manage.py run")
