# Test Plan – Web Application

**Note:** All company-specific names, versions, credentials, file paths, IP addresses and hardware details have been removed.

## 1. LOGIN TESTS

### Authentication Test
**Purpose:** Verify successful login and redirection to dashboard.
**Steps:**
1. Navigate to login page.
2. Enter valid username and password.
3. Click Login button.
4. Verify user reaches dashboard with no errors.

**Success Criteria:** Dashboard loads showing active items. 
**Also tested:** Invalid username/password combinations (error message shown).

### Logout Test
**Purpose:** Verify user can log out successfully.
**Steps:**
1. Open user menu.
2. Click Logout.

**Success Criteria:** Redirected to login page.

### View Password Test
**Purpose:** Verify password visibility toggle works. 
**Steps:**
1. Type password (shown as dots).
2. Click eye icon to reveal.
3. Click again to hide.

**Success Criteria:** Password can be shown and hidden.

## 2. COMMUNICATION TESTS (Generalised for Device Unit)

**Purpose:** Verify communication can be established between Control System and Device Unit.
**Steps (high-level):**
1. Add network.
2. Add device with correct details.
3. Ensure devices are on same network (simulated check).
4. Restart service.

**Success Criteria:** Communication established, status shows IDLE/Ready. Device Unit state updates (e.g., comms indicator on).
**Note:** Hardware-specific steps (e.g., pinging, encryption) are manual/simulated in automation to avoid real interactions.

## 3. BLAST CARD MANAGEMENT (Generalised)

**Purpose:** Verify user can Add, Archive, Delete, Search and Activate cards.
**Steps (example for Active Cards):**
1. Navigate to Cards section.
2. Click Add Card.
3. Search, select using checkboxes.
4. Archive / Delete selected cards.

**Success Criteria:** Cards move between Active / Archived lists, search works, buttons enable correctly.

## 4. USER MANAGEMENT TESTS

**Purpose:** Full CRUD operations on users.
**Tests included:**
- View all users
- Add new user (with validation)
- Edit user (username not editable)
- Delete single / multiple users
- Reset password
- Search by username / name

**Success Criteria:** All operations complete without errors, required fields enforced.

## 5. NETWORK, GROUP, RECIPIENT, DEVICE MANAGEMENT
(Similar CRUD pattern for each entity)

**Tests covered:**
- View, Add, Edit, Delete (single & bulk)
- Search functionality
- Unique name validation

## 6. DASHBOARD, DEVICE DETAILS, REPORTS, FIRMWARE, etc.
**Key tests automated:**
- System alerts display
- Device selection / de-selection
- Arm / Blast commands (UI flow only)
- Channel status colours
- Events log refresh
- Report generation & export (Events, Blast, Network)
- Firmware upload simulation
- Remote access simulation
- Device Unit interactions (communication, state transitions)

**Full manual test plan structure preserved** – only sensitive data removed.
