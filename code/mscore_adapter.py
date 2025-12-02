"""
Adapter for MSCoRe benchmark to MaAS system
Author: Pavan Patel
"""

import json
import logging
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class MSCoReExample:
    """Dataclass for MSCoRe example"""
    question_id: str
    question: str
    answer: str
    reasoning_steps: List[str]
    domain: str
    difficulty: str

class MSCoReAdapter:
    """Adapter class for converting MSCoRe format to MaAS format"""
    
    def __init__(self, mscore_data_path: str):
        self.data_path = mscore_data_path
        self.examples = []
        self.load_data()
        
    def load_data(self):
        """Load MSCoRe dataset"""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                
            for item in data['examples']:
                example = MSCoReExample(
                    question_id=item['id'],
                    question=item['question'],
                    answer=item['answer'],
                    reasoning_steps=item.get('reasoning_steps', []),
                    domain=item.get('domain', 'general'),
                    difficulty=item.get('difficulty', 'medium')
                )
                self.examples.append(example)
                
            logging.info(f"Loaded {len(self.examples)} examples from MSCoRe")
            
        except Exception as e:
            logging.error(f"Error loading MSCoRe data: {e}")
            raise
    
    def convert_to_maas_format(self, example: MSCoReExample) -> Dict[str, Any]:
        """Convert MSCoRe example to MaAS input format"""
        
        maas_input = {
            "id": example.question_id,
            "question": example.question,
            "expected_answer": example.answer,
            "metadata": {
                "domain": example.domain,
                "difficulty": example.difficulty,
                "source": "MSCoRe",
                "reasoning_steps": example.reasoning_steps
            }
        }
        
        return maas_input
    
    def batch_convert(self, examples: List[MSCoReExample] = None) -> List[Dict]:
        """Convert multiple examples"""
        if examples is None:
            examples = self.examples
            
        maas_inputs = []
        for example in examples:
            maas_inputs.append(self.convert_to_maas_format(example))
            
        return maas_inputs
    
    def analyze_question_type(self, question: str) -> Dict[str, bool]:
        """Analyze question to determine needed agents"""
        
        analysis = {
            "has_arithmetic": self._has_arithmetic(question),
            "has_temporal": self._has_temporal(question),
            "has_logical": self._has_logical(question),
            "has_spatial": self._has_spatial(question),
            "has_commonsense": self._has_commonsense(question),
            "requires_multi_step": self._requires_multi_step(question)
        }
        
        return analysis
    
    def _has_arithmetic(self, question: str) -> bool:
        """Check if question contains arithmetic"""
        arithmetic_keywords = ['+', '-', '×', '*', '/', '÷', 'percent', 
                              'percentage', 'sum', 'total', 'average']
        return any(keyword in question.lower() for keyword in arithmetic_keywords)
    
    def _has_temporal(self, question: str) -> bool:
        """Check if question contains temporal reasoning"""
        temporal_keywords = ['day', 'month', 'year', 'hour', 'minute', 
                            'second', 'date', 'time', 'age', 'born']
        return any(keyword in question.lower() for keyword in temporal_keywords)
    
    def _has_logical(self, question: str) -> bool:
        """Check if question contains logical reasoning"""
        logical_keywords = ['if', 'then', 'and', 'or', 'not', 'all', 
                           'some', 'none', 'implies', 'therefore']
        return any(keyword in question.lower() for keyword in logical_keywords)
    
    def _has_spatial(self, question: str) -> bool:
        """Check if question contains spatial reasoning"""
        spatial_keywords = ['square', 'circle', 'triangle', 'perimeter', 
                           'area', 'volume', 'distance', 'angle']
        return any(keyword in question.lower() for keyword in spatial_keywords)
    
    def _has_commonsense(self, question: str) -> bool:
        """Check if question requires commonsense knowledge"""
        commonsense_keywords = ['capital', 'president', 'country', 'city',
                               'person', 'animal', 'color', 'shape']
        return any(keyword in question.lower() for keyword in commonsense_keywords)
    
    def _requires_multi_step(self, question: str) -> bool:
        """Check if question requires multiple steps"""
        step_indicators = ['then', 'after', 'next', 'first', 'second',
                          'finally', 'later', 'subsequently']
        return any(indicator in question.lower() for indicator in step_indicators)