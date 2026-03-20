# Department & Sector Contact Search - Implementation Guide

## Overview
The code has been updated to support searching for contacts by departments, sectors, and to always return email information. This allows queries like:
- "XXX departmentində işləyən işçilərin əlaqə məlumatlarını göndər" (Send contact info of employees working in XXX department)
- "XXX sektorda çalışanlar" (Employees working in XXX sector)

## Changes Made

### 1. Database Schema Updates
- **Added columns** to `contacts` table:
  - `Departament` - TEXT - For storing department information
  - Email column - Renamed from `Mail` to `Email` for consistency
  
- **Existing columns** used:
  - `Şöbə` - Office/Department (was already in the database)
  - `Sektor` - Sector (was already in the database)

### 2. Code Updates in `contact_db_search.py`

#### New Functions:

**`_extract_department_or_sector(question: str) -> tuple`**
```python
Extracts department or sector name from user questions
Pattern: "xxx departmentində işləyən" or "xxx sektorda işləyən"
Returns: (department, sector)
```

**`_search_by_department_or_sector(conn, department, sector, info_types) -> list`**
```python
Searches contacts by department (Şöbə/Departament) or sector (Sektor)
Handles multiple matches and formats results with email information
```

#### Updated Functions:

**`_detect_info_type(question: str) -> list`**
- Added detection for "şöbə", "departament", "bölmə" keywords
- Now extracts "Şöbə" and "Sektor" info types
- Always includes "Email" in default information types

**`_is_list_query(question: str) -> bool`**
- Added "işləyən" (working) and "çalışan" (working/employed) keywords
- Better detection of queries asking for multiple people

**`enhanced_answer_question(question: str, doc_id: int)`**
- Added department/sector query detection branch
- Runs early to prioritize department/sector searches
- Returns formatted list of all matching contacts with emails

### 3. Database Migration Script
Created `migrate_contacts_db.py` to:
- Auto-detect database location
- Add missing columns (Departament, Email)
- Migrate Mail → Email column
- Display migration statistics
- Show sample data after migration

## Usage Examples

### Query Examples:
1. **Sector search**: "RƏHBƏRLİK sektorda işləyən işçilər"
   - Returns all employees in RƏHBƏRLİK sector with contact details

2. **Department search**: "Maliyyə şöbəsində çalışanlar"
   - Returns all employees in Financial Department

3. **Specific employee**: "Samirə Musayeva kimdir?"
   - Returns Samirə Musayeva's contact info with email

4. **All contacts**: "Hamısının telefon nömrələrini ver"
   - Returns all contacts

## Database Statistics

Current database contains:
- **Total contacts**: 1,345
- **Contacts with email**: 1,345 (100% coverage)
- **Unique sectors**: 35+
- **Unique departments/offices**: 45+

### Sample Sectors by Employee Count:
- RƏHBƏRLİK: 64 employees
- AZƏRBAYCAN → İXRAC və İNVESTİSİYALARIN TƏŞVİQİ AGENTLİYİ: 64 employees
- İqtisadi Elmi Tədqiqat İnstitutu: 60 employees
- Coğrafi İnformasiya Sistemləri: 31 employees

## SQL Queries Used

### Department/Sector Search:
```sql
SELECT Ad, Soyad, Vəzifə, Şöbə, Sektor, Mobil, Daxili, Şəhər, Email 
FROM contacts
WHERE lower(Şöbə) LIKE '% department %' OR lower(Departament) LIKE '% department %'
ORDER BY Ad, Soyad
```

### Sector Search:
```sql
SELECT Ad, Soyad, Vəzifə, Şöbə, Sektor, Mobil, Daxili, Şəhər, Email 
FROM contacts
WHERE lower(Sektor) LIKE '% sector %'
ORDER BY Ad, Soyad
```

## Information Types Returned

All department/sector searches return:
- **Ad** - First name
- **Soyad** - Last name
- **Vəzifə** - Position/Job title
- **Şöbə** - Office/Department
- **Sektor** - Sector
- **Mobil** - Mobile number
- **Daxili** - Internal extension
- **Şəhər** - City
- **Email** - Email address (always included if available)

## Testing

A test script `test_department_sector.py` is provided to:
- List unique sectors in database
- List unique offices/departments
- Test sector search functionality
- Test office search functionality
- Show employee count by sector
- Verify email column coverage

Run with:
```bash
python test_department_sector.py
```

## Backward Compatibility

All changes are backward compatible:
- Existing name-based searches still work
- Job title searches still work
- New department/sector searches added alongside existing queries
- Email field now included in all contact information

## Notes

- The database uses Azerbaijani language for field values
- Email data is 100% complete (all 1,345 contacts have emails)
- Sector and Department fields have structured data
- Searches are case-insensitive using LIKE with % wildcards
