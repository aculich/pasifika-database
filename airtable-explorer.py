#!/usr/bin/env python3
"""
Airtable Schema Explorer
Safely connects to Airtable and explores the schema before any data export
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm

class AirtableExplorer:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        self.api_key = os.getenv('AIRTABLE_API_KEY')
        if not self.api_key:
            raise ValueError("AIRTABLE_API_KEY not found in .env file")
        
        # Verify API key format (should start with 'pat')
        if not self.api_key.startswith('pat'):
            raise ValueError("Invalid API key format. Should start with 'pat'")
        
        self.base_dir = Path(__file__).parent
        self.exploration_dir = self.base_dir / "airtable_exploration"
        self.exploration_dir.mkdir(exist_ok=True)
        
        print(f"🔑 API Key loaded: {self.api_key[:10]}...{self.api_key[-10:]}")
    
    def test_connection(self):
        """Test the Airtable API connection"""
        print("🔍 Testing Airtable API connection...")
        
        try:
            with tqdm(total=1, desc="Testing connection", unit="request") as pbar:
                response = requests.get(
                    "https://api.airtable.com/v0/meta/bases",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=10
                )
                pbar.update(1)
            
            if response.status_code == 200:
                print("✅ Connection successful!")
                return True
            elif response.status_code == 401:
                print("❌ Authentication failed. Please check your API key.")
                return False
            elif response.status_code == 403:
                print("❌ Access forbidden. API key may not have required permissions.")
                return False
            else:
                print(f"❌ Connection failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print("❌ Connection timeout. Please check your internet connection.")
            return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def get_bases(self):
        """Get all accessible Airtable bases"""
        print("📁 Discovering accessible Airtable bases...")
        
        try:
            with tqdm(total=1, desc="Fetching bases", unit="request") as pbar:
                response = requests.get(
                    "https://api.airtable.com/v0/meta/bases",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                pbar.update(1)
            
            if response.status_code == 200:
                bases = response.json().get('bases', [])
                print(f"✅ Found {len(bases)} accessible bases")
                
                # Save bases list
                bases_file = self.exploration_dir / "accessible_bases.json"
                with open(bases_file, 'w') as f:
                    json.dump(bases, f, indent=2)
                print(f"📄 Bases list saved to {bases_file}")
                
                return bases
            else:
                print(f"❌ Error getting bases: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error fetching bases: {e}")
            return []
    
    def explore_base_schema(self, base_id, base_name):
        """Explore the schema of a specific base"""
        print(f"\n📋 Exploring schema for base: {base_name}")
        print(f"   Base ID: {base_id}")
        
        try:
            with tqdm(total=1, desc="Fetching schema", unit="request") as pbar:
                response = requests.get(
                    f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                pbar.update(1)
            
            if response.status_code == 200:
                schema = response.json()
                tables = schema.get('tables', [])
                
                print(f"✅ Found {len(tables)} tables in this base")
                
                # Save schema
                schema_file = self.exploration_dir / f"{base_name}_schema.json"
                with open(schema_file, 'w') as f:
                    json.dump(schema, f, indent=2)
                print(f"📄 Schema saved to {schema_file}")
                
                # Display table summary
                print(f"\n📊 Table Summary for '{base_name}':")
                print("=" * 60)
                
                for i, table in enumerate(tables, 1):
                    table_name = table.get('name', 'Unnamed')
                    table_id = table.get('id', 'Unknown')
                    fields = table.get('fields', [])
                    
                    print(f"{i}. {table_name}")
                    print(f"   ID: {table_id}")
                    print(f"   Fields: {len(fields)}")
                    
                    # Show field types
                    field_types = {}
                    for field in fields:
                        field_type = field.get('type', 'unknown')
                        field_types[field_type] = field_types.get(field_type, 0) + 1
                    
                    if field_types:
                        type_summary = ", ".join([f"{count} {ftype}" for ftype, count in field_types.items()])
                        print(f"   Field types: {type_summary}")
                    print()
                
                return schema
            else:
                print(f"❌ Error getting schema: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error exploring schema: {e}")
            return None
    
    def estimate_data_volume(self, base_id, base_name):
        """Estimate the data volume in a base"""
        print(f"\n📊 Estimating data volume for base: {base_name}")
        
        try:
            schema = self.explore_base_schema(base_id, base_name)
            if not schema:
                return None
            
            tables = schema.get('tables', [])
            total_estimated_records = 0
            
            print(f"🔍 Sampling records from {len(tables)} tables...")
            
            for table in tqdm(tables, desc="Sampling tables", unit="table"):
                table_id = table.get('id')
                table_name = table.get('name', 'Unnamed')
                
                try:
                    # Get first page to estimate record count
                    response = requests.get(
                        f"https://api.airtable.com/v0/{base_id}/{table_id}",
                        headers={"Authorization": f"Bearer {self.api_key}"},
                        params={"pageSize": 1}  # Just get 1 record to test
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        records = data.get('records', [])
                        offset = data.get('offset')
                        
                        if records:
                            # If there's an offset, there are more records
                            # This is a rough estimate
                            estimated_records = 1 if not offset else 100
                            total_estimated_records += estimated_records
                            
                            print(f"   📄 {table_name}: ~{estimated_records} records")
                        else:
                            print(f"   📄 {table_name}: 0 records")
                    else:
                        print(f"   ❌ {table_name}: Error accessing data")
                        
                except Exception as e:
                    print(f"   ❌ {table_name}: Error - {e}")
            
            print(f"\n📊 Total estimated records: {total_estimated_records}")
            print(f"⏱️  Estimated export time: {total_estimated_records * 0.02:.1f} seconds")
            
            return total_estimated_records
            
        except Exception as e:
            print(f"❌ Error estimating data volume: {e}")
            return None
    
    def create_exploration_summary(self, bases):
        """Create a summary of the exploration"""
        print("\n📋 Creating exploration summary...")
        
        summary = {
            'exploration_timestamp': datetime.now().isoformat(),
            'api_key_masked': f"{self.api_key[:10]}...{self.api_key[-10:]}",
            'total_bases': len(bases),
            'bases': []
        }
        
        for base in bases:
            base_id = base['id']
            base_name = base['name']
            
            print(f"📊 Analyzing base: {base_name}")
            
            # Get schema
            schema = self.explore_base_schema(base_id, base_name)
            if schema:
                tables = schema.get('tables', [])
                
                base_summary = {
                    'base_id': base_id,
                    'base_name': base_name,
                    'table_count': len(tables),
                    'tables': []
                }
                
                for table in tables:
                    table_summary = {
                        'table_id': table.get('id'),
                        'table_name': table.get('name'),
                        'field_count': len(table.get('fields', [])),
                        'field_types': {}
                    }
                    
                    # Count field types
                    for field in table.get('fields', []):
                        field_type = field.get('type', 'unknown')
                        table_summary['field_types'][field_type] = table_summary['field_types'].get(field_type, 0) + 1
                    
                    base_summary['tables'].append(table_summary)
                
                summary['bases'].append(base_summary)
        
        # Save summary
        summary_file = self.exploration_dir / "exploration_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"✅ Exploration summary saved to {summary_file}")
        
        # Display summary
        print(f"\n🎉 Exploration Complete!")
        print("=" * 60)
        print(f"📊 Total bases discovered: {len(bases)}")
        print(f"📁 Exploration files saved to: {self.exploration_dir}")
        print(f"📄 Summary file: {summary_file}")
        
        return summary
    
    def run_exploration(self):
        """Run the complete exploration process"""
        print("🚀 Starting Airtable exploration...")
        print("=" * 60)
        
        # Step 1: Test connection
        if not self.test_connection():
            print("❌ Connection test failed. Stopping exploration.")
            return False
        
        # Step 2: Get bases
        bases = self.get_bases()
        if not bases:
            print("❌ No bases found. Stopping exploration.")
            return False
        
        # Step 3: Explore each base
        print(f"\n🔍 Exploring {len(bases)} bases...")
        for base in bases:
            base_id = base['id']
            base_name = base['name']
            
            # Estimate data volume for each base
            self.estimate_data_volume(base_id, base_name)
        
        # Step 4: Create summary
        summary = self.create_exploration_summary(bases)
        
        print(f"\n✅ Exploration complete! Check {self.exploration_dir} for detailed results.")
        
        return True

if __name__ == "__main__":
    try:
        explorer = AirtableExplorer()
        explorer.run_exploration()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your .env file and ensure AIRTABLE_API_KEY is set correctly.")
