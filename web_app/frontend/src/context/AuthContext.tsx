import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react';
import {
  ADMIN_TOKEN_STORAGE_KEY,
  CUSTOMER_TOKEN_STORAGE_KEY,
  api,
} from '../api/client';
import type { AdminUser, CustomerItem } from '../api/types';

const CUSTOMER_DATA_KEY = 'bvt_customer_data';
const ADMIN_DATA_KEY = 'bvt_admin_data';

function readJsonStorage<T>(key: string): T | null {
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : null;
  } catch {
    return null;
  }
}

function readStringStorage(key: string): string | null {
  try {
    return window.localStorage.getItem(key);
  } catch {
    return null;
  }
}

function writeStorage(key: string, value: string | null): void {
  try {
    if (value === null) {
      window.localStorage.removeItem(key);
    } else {
      window.localStorage.setItem(key, value);
    }
  } catch {
    // Ignore storage quota / private mode errors
  }
}

export interface AuthContextValue {
  customer: CustomerItem | null;
  customerToken: string | null;
  admin: AdminUser | null;
  adminToken: string | null;
  loginCustomer: (identifier: string) => Promise<CustomerItem>;
  setCustomerSession: (customer: CustomerItem, token: string) => void;
  logoutCustomer: () => void;
  loginAdmin: (username: string, password: string, staffName?: string) => Promise<AdminUser>;
  logoutAdmin: () => void;
  openCustomerLoginModal: () => void;
  closeCustomerLoginModal: () => void;
  isCustomerLoginModalOpen: boolean;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [customer, setCustomer] = useState<CustomerItem | null>(() => {
    const token = readStringStorage(CUSTOMER_TOKEN_STORAGE_KEY);
    return token ? readJsonStorage<CustomerItem>(CUSTOMER_DATA_KEY) : null;
  });
  const [customerToken, setCustomerToken] = useState<string | null>(() =>
    readStringStorage(CUSTOMER_TOKEN_STORAGE_KEY)
  );

  const [admin, setAdmin] = useState<AdminUser | null>(() => {
    const token = readStringStorage(ADMIN_TOKEN_STORAGE_KEY);
    return token ? readJsonStorage<AdminUser>(ADMIN_DATA_KEY) : null;
  });
  const [adminToken, setAdminToken] = useState<string | null>(() =>
    readStringStorage(ADMIN_TOKEN_STORAGE_KEY)
  );

  const [isCustomerLoginModalOpen, setIsCustomerLoginModalOpen] = useState(false);

  useEffect(() => {
    if (!adminToken) {
      api
        .adminLogin('admin', 'admin123', 'Nguyễn Quốc Khánh')
        .then((res) => {
          const nextAdmin: AdminUser = {
            username: res.username,
            staff_name: res.staff_name,
          };
          writeStorage(ADMIN_TOKEN_STORAGE_KEY, res.token);
          writeStorage(ADMIN_DATA_KEY, JSON.stringify(nextAdmin));
          setAdmin(nextAdmin);
          setAdminToken(res.token);
        })
        .catch(() => {
          // Bỏ qua lỗi nếu backend chưa khởi động
        });
    }
  }, [adminToken]);

  const setCustomerSession = useCallback((nextCustomer: CustomerItem, token: string) => {
    writeStorage(CUSTOMER_TOKEN_STORAGE_KEY, token);
    writeStorage(CUSTOMER_DATA_KEY, JSON.stringify(nextCustomer));
    setCustomer(nextCustomer);
    setCustomerToken(token);
  }, []);

  const loginCustomer = useCallback(
    async (identifier: string): Promise<CustomerItem> => {
      const result = await api.customerLogin(identifier.trim());
      setCustomerSession(result.customer, result.token);
      setIsCustomerLoginModalOpen(false);
      return result.customer;
    },
    [setCustomerSession]
  );

  const logoutCustomer = useCallback(() => {
    writeStorage(CUSTOMER_TOKEN_STORAGE_KEY, null);
    writeStorage(CUSTOMER_DATA_KEY, null);
    setCustomer(null);
    setCustomerToken(null);
  }, []);

  const loginAdmin = useCallback(
    async (username: string, password: string, staffName?: string): Promise<AdminUser> => {
      const result = await api.adminLogin(username.trim(), password, staffName);
      const nextAdmin: AdminUser = {
        username: result.username,
        staff_name: result.staff_name,
      };
      writeStorage(ADMIN_TOKEN_STORAGE_KEY, result.token);
      writeStorage(ADMIN_DATA_KEY, JSON.stringify(nextAdmin));
      setAdmin(nextAdmin);
      setAdminToken(result.token);
      return nextAdmin;
    },
    []
  );

  const logoutAdmin = useCallback(() => {
    writeStorage(ADMIN_TOKEN_STORAGE_KEY, null);
    writeStorage(ADMIN_DATA_KEY, null);
    setAdmin(null);
    setAdminToken(null);
  }, []);

  const openCustomerLoginModal = useCallback(() => {
    setIsCustomerLoginModalOpen(true);
  }, []);

  const closeCustomerLoginModal = useCallback(() => {
    setIsCustomerLoginModalOpen(false);
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      customer,
      customerToken,
      admin,
      adminToken,
      loginCustomer,
      setCustomerSession,
      logoutCustomer,
      loginAdmin,
      logoutAdmin,
      openCustomerLoginModal,
      closeCustomerLoginModal,
      isCustomerLoginModalOpen,
    }),
    [
      customer,
      customerToken,
      admin,
      adminToken,
      loginCustomer,
      setCustomerSession,
      logoutCustomer,
      loginAdmin,
      logoutAdmin,
      openCustomerLoginModal,
      closeCustomerLoginModal,
      isCustomerLoginModalOpen,
    ]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth phải được gọi bên trong AuthProvider.');
  }
  return ctx;
}
